from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

# ===============================
# Base schemas
# ===============================

class AlarmBase(BaseModel):
    tag: str = Field(
        ...,
        json_schema_extra={"example": "PUMP_01"}
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={"example": "High pressure detected"}
    )
    severity: int = Field(
        ...,
        ge=1,
        le=4,
        json_schema_extra={"example": 3}
    )
    status: str = Field(
        ...,
        json_schema_extra={"example": "ACTIVE"}
    )
    event_time: datetime


# ===============================
# Response schemas
# ===============================

class AlarmResponse(AlarmBase):
    id: int
    source_system: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlarmListResponse(BaseModel):
    data: List[AlarmResponse]
    total: int
    limit: int
    offset: int


# ===============================
# Metrics schemas
# ===============================

class TopTagMetric(BaseModel):
    tag: str
    total_events: int


class TopTagsResponse(BaseModel):
    data: List[TopTagMetric]