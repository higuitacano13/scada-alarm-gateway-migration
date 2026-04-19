
from sqlalchemy import (
    Column, Integer, String, DateTime, BigInteger, ForeignKey
)
from sqlalchemy.orm import relationship
from db.base import Base


class AlarmEvent(Base):
    __tablename__ = "alarm_event"

    alarm_event_id = Column(BigInteger, primary_key=True, index=True)
    tag = Column(String(100), nullable=False)
    description = Column(String(255))
    severity_id = Column(Integer, ForeignKey("alarm_severity.severity_id"))
    source_system_id = Column(Integer, ForeignKey("source_system.source_system_id"))
    event_time = Column(DateTime, nullable=False)
    cleared_time = Column(DateTime)
    status = Column(String(20), nullable=False)
    raw_payload_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    severity = relationship("AlarmSeverity")
    source_system = relationship("SourceSystem")
