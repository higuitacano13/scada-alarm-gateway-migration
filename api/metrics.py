from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from dependencies.alarm_dependencies import get_alarm_service
from models.schemas import TopTagsResponse
from services.alarm_service import AlarmService

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/top-tags", response_model=TopTagsResponse)
def top_tags(
    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    limit: int = Query(10, ge=1, le=50),
    service: AlarmService = Depends(get_alarm_service)
):
    try:
        return service.top_tags(
        from_date=from_date,
        to_date=to_date,
        limit=limit
    )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
