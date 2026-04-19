from db.base import Base
from sqlalchemy import (
    Column, Integer, String
)

class AlarmSeverity(Base):
    __tablename__ = "alarm_severity"

    severity_id = Column(Integer, primary_key=True)
    severity_code = Column(String(20), unique=True, nullable=False)
    severity_level = Column(Integer, nullable=False)
