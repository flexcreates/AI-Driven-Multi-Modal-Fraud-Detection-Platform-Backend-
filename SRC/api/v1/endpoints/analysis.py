from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from SRC.database.session import get_db
from SRC.models.analysis import AnalysisRecord
from SRC.models.user import User
from SRC.schemas.analysis import TextAnalysisRequest, UrlAnalysisRequest, AnalysisResponse
from SRC.services import ai_service, risk_engine
from SRC.core.security import create_access_token # Just import something to check, actually we need get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from SRC.config.settings import settings
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

router = APIRouter()

@router.post("/text", response_model=AnalysisResponse)
async def analyze_text_endpoint(request: TextAnalysisRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 1. AI Analysis
    ai_result = await ai_service.analyze_text(request.content)
    
    # 2. Risk Engine
    risk_result = risk_engine.calculate_risk_score(ai_result, "TEXT")
    
    # 3. Save to DB
    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="TEXT",
        input_hash=str(hash(request.content)), # Simple hash
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED"
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

@router.post("/url", response_model=AnalysisResponse)
async def analyze_url_endpoint(request: UrlAnalysisRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    ai_result = await ai_service.analyze_url(request.url)
    risk_result = risk_engine.calculate_risk_score(ai_result, "URL")
    
    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="URL",
        input_hash=str(hash(request.url)),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED"
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

@router.post("/file", response_model=AnalysisResponse)
async def analyze_file_endpoint(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    ai_result = await ai_service.analyze_file(file.filename, content)
    risk_result = risk_engine.calculate_risk_score(ai_result, "FILE")
    
    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="DOCUMENT", # Mapping FILE to DOCUMENT as per schema
        input_hash=str(hash(content)),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED"
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record
