from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from SRC.database.base import Base

class AnalysisRecord(Base):
    __tablename__ = "analysis_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    input_type = Column(String, nullable=False) # TEXT, URL, DOCUMENT, IMAGE
    input_hash = Column(String, index=True) # Matches input_hash in schema
    risk_score = Column(Float)
    risk_level = Column(String) # LOW, MEDIUM, HIGH
    decision = Column(String) # ALLOW, FLAG, BLOCK
    details = Column(JSON) # To store extended info (risk components)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="analyses")
