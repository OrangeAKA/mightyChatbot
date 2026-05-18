import structlog
from app.services import llm
from app.services.orders import reply_for

logger = structlog.get_logger()
LOW_CONFIDENCE_THRESHOLD = 0.7

# STUB: refund_policy, talk_to_agent, account_help return placeholders — implemented Day 3+
_STUBS = {
    "refund_policy": "Our standard refund policy allows returns within 30 days. (Full lookup coming soon.)",
    "talk_to_agent": "I'll connect you with a human agent shortly. (Handoff flow coming soon.)",
    "account_help": "I can help with account questions. (Account lookup coming soon.)",
    "out_of_scope": "I can help with order status, refund policies, and account questions. What would you like?",
}


async def route(message: str) -> dict:
    classification = await llm.classify(message)
    intent: str = classification["intent"]
    confidence: float = classification["confidence"]
    order_id: str | None = classification.get("order_id")
    low_confidence = confidence < LOW_CONFIDENCE_THRESHOLD

    if low_confidence:
        logger.warning("low_confidence_intent", intent=intent, confidence=confidence)

    if intent == "order_status":
        if order_id:
            reply = reply_for(order_id)
        else:
            reply = "I can look up your order status. Could you share your order number (e.g. ORD-001)?"
    else:
        reply = _STUBS.get(intent, "I'm not sure how to help with that.")

    return {
        "reply": reply,
        "intent": intent,
        "confidence": round(confidence, 3),
        "low_confidence": low_confidence,
    }
