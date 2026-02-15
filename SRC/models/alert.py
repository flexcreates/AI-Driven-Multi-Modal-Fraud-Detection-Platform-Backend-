from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from SRC.database.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analysis_logs.id", ondelete="CASCADE"))
    alert_type = Column(String(100), nullable=False)
    sent_to = Column(String(255), nullable=True)
    status = Column(String(50), default="PENDING")  # PENDING, SENT, FAILED
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analysis = relationship("AnalysisRecord", backref="alerts")
