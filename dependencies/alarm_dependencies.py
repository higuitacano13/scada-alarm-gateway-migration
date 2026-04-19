from fastapi import Depends
from repositories.alarm_repository import AlarmRepository
from services.alarm_service import AlarmService

def get_alarm_repository():
    repo = AlarmRepository()
    try:
        yield repo
    finally:
        repo.close()

def get_alarm_service(
    repo: AlarmRepository = Depends(get_alarm_repository)
):
    return AlarmService(repo)