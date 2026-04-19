from typing import Optional, Tuple, List
from datetime import datetime

from fastapi.params import Query
from repositories.alarm_repository import AlarmRepository


class AlarmService:

    def __init__(self, repo: AlarmRepository):
        self.repo = repo

    def get_alarms(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        severity: Optional[int],
        tag: Optional[str],
        limit: int,
        offset: int
    ) -> Tuple[List, int]:

        if from_date and to_date and from_date > to_date:
            raise ValueError("from_date must be earlier than to_date")

        return self.repo.get_alarms(
            start_time=from_date,
            end_time=to_date,
            severity=severity,
            tag=tag,
            limit=limit,
            offset=offset
        )

    def top_tags(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        limit: int,
    ):
        data = self.repo.get_top_tags(
            start_time=from_date,
            end_time=to_date,
            limit=limit
        )
        
        return {"data": data}
    