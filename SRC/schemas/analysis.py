from typing import Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AnalysisRequest(BaseModel):
    content: str # For Text/URL
    # For file, we'll use UploadFile in the endpoint, this is for JSON payload if any

class TextAnalysisRequest(BaseModel):
    content: str

class UrlAnalysisRequest(BaseModel):
    url: str

class AnalysisResponse(BaseModel):
    id: UUID
    status: str
    input_type: str
    input_hash: Optional[str] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    decision: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
