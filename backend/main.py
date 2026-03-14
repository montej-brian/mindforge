"""
MINDFORGE — FastAPI Application Entry Point
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import health, voice, agents, tasks
from api.websockets import router as ws_router
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup / shutdown lifecycle."""
    logger.info("🧠 MINDFORGE starting up...")
    
    # Initialize database tables
    from database import init_db
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

    # Initialize browser session pool, etc. here
    yield
    logger.info("🛑 MINDFORGE shutting down...")


app = FastAPI(
    title="MINDFORGE API",
    description="Voice-controlled multi-agent AI system for automating online assignments",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(ws_router, tags=["WebSocket"])


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "MINDFORGE API is running", "docs": "/api/docs"}
