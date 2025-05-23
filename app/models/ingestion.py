from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Ingestion(Base):
    __tablename__ = "ingestions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    status = Column(String, default="pending")  # pending, in_progress, completed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    document = relationship("Document", back_populates="ingestions")