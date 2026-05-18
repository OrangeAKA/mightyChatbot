import structlog
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_router import route

logger = structlog.get_logger()
router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
    low_confidence: bool


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    logger.info("chat_request", message_preview=req.message[:80])
    result = await route(req.message)
    return result
