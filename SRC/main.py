from fastapi import FastAPI
from SRC.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

from sqlalchemy.sql import text
from SRC.database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        
    return {
        "status": "UP",
        "database": db_status,
        "models": "loaded" # Placeholder until models are integrated
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("SRC.main:app", host="0.0.0.0", port=8000, reload=True)
