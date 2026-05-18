import structlog
from fastapi import APIRouter

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    logger.info("health_check")
    return {"status": "ok"}
