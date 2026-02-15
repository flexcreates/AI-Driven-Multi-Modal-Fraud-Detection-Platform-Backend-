from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from SRC.database.base import Base


class RiskComponent(Base):
    __tablename__ = "risk_components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analysis_logs.id", ondelete="CASCADE"))
    text_score = Column(Float, default=0.0)
    url_score = Column(Float, default=0.0)
    metadata_score = Column(Float, default=0.0)
    injection_score = Column(Float, default=0.0)
    credential_score = Column(Float, default=0.0)
    malware_score = Column(Float, default=0.0)

    analysis = relationship("AnalysisRecord", backref="risk_components")
