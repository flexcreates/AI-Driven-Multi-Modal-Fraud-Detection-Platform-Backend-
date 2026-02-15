from fastapi import FastAPI
from SRC.config.settings import settings
from SRC.logs.logger import get_logger

logger = get_logger("main")

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

from sqlalchemy.sql import text
from SRC.database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")

from SRC.api.docs.auth import router as auth_router
from SRC.api.v1.endpoints.analysis import router as analysis_router

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(analysis_router, prefix="/analyze", tags=["Analysis"])

@app.get("/health")
def health_check(): # Removed db dependency for simple check, or keep it if needed. kept simple for now
    return {"status": "UP"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server...")
    uvicorn.run("SRC.main:app", host="0.0.0.0", port=8000, reload=True)
