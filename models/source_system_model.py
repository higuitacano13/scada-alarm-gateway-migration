
from db.base import Base
from sqlalchemy import (
    Column, Integer, String
)

class SourceSystem(Base):
    __tablename__ = "source_system"

    source_system_id = Column(Integer, primary_key=True)
    system_name = Column(String(50), unique=True, nullable=False)


