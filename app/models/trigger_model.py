from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

class Trigger(Base):
    __tablename__ = "trigger"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String)
    device_id = Column(UUID(as_uuid=True), ForeignKey("device.id"), nullable=False)
    notif_state = Column(Boolean)
    last_value = Column(Float)
    notif_value = Column(Float)
    check_clock = Column(Integer)
    write_clock = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.utcnow())