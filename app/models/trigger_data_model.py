from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

class TriggerData(Base):
    __tablename__ = 'trigger_data'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    value = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
