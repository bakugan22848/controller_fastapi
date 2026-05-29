from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

class Controller(Base):
    __tablename__ = 'controller'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String)
    device_id = Column(UUID(as_uuid=True), ForeignKey("device.id"), nullable=False)
    trigger_id = Column(UUID(as_uuid=True), ForeignKey("trigger.id"))
    trigger_vector = Column(String)
    last_state = Column(Boolean)
    trigger_value = Column(Integer)
    is_automatic = Column(Boolean)
    pin = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.utcnow())
