import time
import structlog
from anthropic import AsyncAnthropic
from app.config import settings

logger = structlog.get_logger()

INTENTS = ["order_status", "refund_policy", "talk_to_agent", "account_help", "out_of_scope"]

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


_CLASSIFY_TOOL = {
    "name": "classify_intent",
    "description": (
        "Classify the customer message into one intent category, "
        "extract any order ID present, and score confidence."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "intent": {"type": "string", "enum": INTENTS},
            "confidence": {"type": "number", "description": "0.0–1.0, conservative"},
            "order_id": {
                "type": "string",
                "description": "Order ID if the user mentioned one (e.g. ORD-123). Omit if absent.",
            },
        },
        "required": ["intent", "confidence"],
    },
}

_SYSTEM = (
    "You are an intent classifier for a customer-service chatbot at a rewards platform. "
    "Classify the user message and extract entities. "
    "Score confidence conservatively — ambiguous messages must be below 0.7."
)


async def classify(message: str) -> dict:
    """Classify message intent via Haiku tool-use. Returns {intent, confidence, order_id?}."""
    client = _get_client()
    t0 = time.perf_counter()

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=_SYSTEM,
        messages=[{"role": "user", "content": message}],
        tools=[_CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_intent"},
    )

    latency_ms = round((time.perf_counter() - t0) * 1000)
    tool_block = next(b for b in response.content if b.type == "tool_use")
    result: dict = tool_block.input

    logger.info(
        "llm_call",
        model="claude-haiku-4-5-20251001",
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        latency_ms=latency_ms,
        intent=result.get("intent"),
        confidence=result.get("confidence"),
    )

    return result
