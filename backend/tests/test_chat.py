from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def mock_classify():
    """Patch llm.classify so tests never hit the real Anthropic API."""
    with patch("app.services.intent_router.llm.classify") as m:
        yield m


async def _post(message: str):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.post("/chat", json={"message": message})


async def test_chat_order_status_with_id(mock_classify):
    mock_classify.return_value = {"intent": "order_status", "confidence": 0.95, "order_id": "ORD-001"}
    r = await _post("Where is my order ORD-001?")
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "order_status"
    assert "in transit" in body["reply"]
    assert body["low_confidence"] is False


async def test_chat_order_status_without_id(mock_classify):
    mock_classify.return_value = {"intent": "order_status", "confidence": 0.88}
    r = await _post("I want to check my order")
    assert r.status_code == 200
    body = r.json()
    assert "order number" in body["reply"]


async def test_chat_low_confidence_flagged(mock_classify):
    mock_classify.return_value = {"intent": "out_of_scope", "confidence": 0.55}
    r = await _post("blah blah something unclear")
    assert r.status_code == 200
    assert r.json()["low_confidence"] is True


async def test_chat_out_of_scope(mock_classify):
    mock_classify.return_value = {"intent": "out_of_scope", "confidence": 0.91}
    r = await _post("What is the weather today?")
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "out_of_scope"
    assert body["low_confidence"] is False


async def test_chat_response_schema(mock_classify):
    mock_classify.return_value = {"intent": "refund_policy", "confidence": 0.82}
    r = await _post("Can I get a refund?")
    body = r.json()
    assert set(body.keys()) == {"reply", "intent", "confidence", "low_confidence"}
