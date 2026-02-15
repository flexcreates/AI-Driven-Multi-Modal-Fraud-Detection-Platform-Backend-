import hashlib
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from SRC.database.session import get_db
from SRC.models.analysis import AnalysisRecord
from SRC.models.user import User
from SRC.schemas.analysis import TextAnalysisRequest, UrlAnalysisRequest, AnalysisResponse
from SRC.services import ai_service, risk_engine
from SRC.api.deps import get_current_active_user
from SRC.logs.logger import get_logger

logger = get_logger("api.analysis")

router = APIRouter()


def _sha256_hash(data: bytes | str) -> str:
    """Generate a SHA256 hex digest for input content."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


@router.post("/text", response_model=AnalysisResponse)
async def analyze_text_endpoint(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze text content for fraud indicators."""
    logger.info(f"Text analysis requested by user={current_user.email}")

    # 1. AI Analysis
    ai_result = await ai_service.analyze_text(request.content)

    # 2. Risk Engine
    risk_result = risk_engine.calculate_risk_score(ai_result, "TEXT")

    # 3. Save to DB
    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="TEXT",
        input_hash=_sha256_hash(request.content),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED",
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    logger.info(f"Text analysis completed: id={record.id}, decision={record.decision}")
    return record


@router.post("/url", response_model=AnalysisResponse)
async def analyze_url_endpoint(
    request: UrlAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze a URL for phishing indicators."""
    logger.info(f"URL analysis requested by user={current_user.email}: {request.url}")

    ai_result = await ai_service.analyze_url(request.url)
    risk_result = risk_engine.calculate_risk_score(ai_result, "URL")

    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="URL",
        input_hash=_sha256_hash(request.url),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED",
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    logger.info(f"URL analysis completed: id={record.id}, decision={record.decision}")
    return record


@router.post("/file", response_model=AnalysisResponse)
async def analyze_file_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze a file (PDF/DOCX) for malware and fraud."""
    logger.info(f"File analysis requested by user={current_user.email}: {file.filename}")

    content = await file.read()
    ai_result = await ai_service.analyze_file(file.filename, content)
    risk_result = risk_engine.calculate_risk_score(ai_result, "FILE")

    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="DOCUMENT",
        input_hash=_sha256_hash(content),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED",
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    logger.info(f"File analysis completed: id={record.id}, decision={record.decision}")
    return record


@router.post("/image", response_model=AnalysisResponse)
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze an image/GIF for steganography, metadata anomalies, and embedded text."""
    logger.info(f"Image analysis requested by user={current_user.email}: {file.filename}")

    content = await file.read()
    ai_result = await ai_service.analyze_image(file.filename, content)
    risk_result = risk_engine.calculate_risk_score(ai_result, "IMAGE")

    record = AnalysisRecord(
        user_id=current_user.id,
        input_type="IMAGE",
        input_hash=_sha256_hash(content),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        decision=risk_result["decision"],
        details=ai_result,
        status="COMPLETED",
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    logger.info(f"Image analysis completed: id={record.id}, decision={record.decision}")
    return record


@router.get("/history", response_model=List[AnalysisResponse])
async def get_analysis_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve the authenticated user's analysis history, most recent first."""
    logger.info(f"History requested by user={current_user.email} (limit={limit})")

    result = await db.execute(
        select(AnalysisRecord)
        .where(AnalysisRecord.user_id == current_user.id)
        .order_by(desc(AnalysisRecord.created_at))
        .limit(min(limit, 100))
    )
    records = result.scalars().all()

    logger.info(f"Returning {len(records)} records for user={current_user.email}")
    return records
