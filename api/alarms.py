from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime
from dependencies.alarm_dependencies import get_alarm_service
from models.schemas import AlarmListResponse
from services.alarm_service import AlarmService

router = APIRouter(prefix="/alarms", tags=["Alarms"])

@router.get("/", response_model=AlarmListResponse)
def get_alarms(
    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    severity: int | None = Query(None, ge=1, le=4),
    tag: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: AlarmService = Depends(get_alarm_service)
):
    try:
        data, total = service.get_alarms(
            from_date=from_date,
            to_date=to_date,
            severity=severity,
            tag=tag,
            limit=limit,
            offset=offset
        )

        return {
            "data": data,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))