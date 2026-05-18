import structlog
import structlog.stdlib
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.health import router as health_router


def configure_logging() -> None:
    # PrintLoggerFactory doesn't expose .name — drop add_logger_name
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    log = structlog.get_logger()
    log.info("startup", app=settings.app_name, env=settings.environment)
    yield
    log.info("shutdown", app=settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tightened to Vercel domain on Day 5 polish
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
