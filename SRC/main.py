from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from SRC.config.settings import settings
from SRC.logs.logger import get_logger
from SRC.middleware.middleware import RequestLoggingMiddleware, CORS_CONFIG

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    logger.info("Application starting up...")
    logger.info(f"Project: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Database: {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend API for AI-Driven Multi-Modal Fraud Detection Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],
    allow_credentials=CORS_CONFIG["allow_credentials"],
    allow_methods=CORS_CONFIG["allow_methods"],
    allow_headers=CORS_CONFIG["allow_headers"],
)
app.add_middleware(RequestLoggingMiddleware)

# --- Routers ---
from SRC.api.docs.auth import router as auth_router
from SRC.api.v1.endpoints.analysis import router as analysis_router

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(analysis_router, prefix="/analyze", tags=["Analysis"])


# --- Health Check ---
@app.get("/health", tags=["System"])
def health_check():
    """Basic health check endpoint."""
    return {"status": "UP", "version": settings.PROJECT_VERSION}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server...")
    uvicorn.run("SRC.main:app", host="0.0.0.0", port=8000, reload=True)
