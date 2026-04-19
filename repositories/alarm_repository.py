from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, select, func
from db.session import SessionLocal
from models.alarm_event_model import AlarmEvent
from models.alarm_severity_model import AlarmSeverity  
from models.source_system_model import SourceSystem 
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class AlarmRepository:

    def __init__(self):
        self.db: Session = SessionLocal()

    def _get_severity_map(self) -> Dict[int, int]:
        """
        Retorna un mapping:
        severity_level -> severity_id
        """
        severities = self.db.execute(
            select(
                AlarmSeverity.severity_level,
                AlarmSeverity.severity_id
            )
        ).all()

        return {level: sid for level, sid in severities}

    def _get_source_system_id(self, system_name: str) -> int:
        source = self.db.execute(
            select(SourceSystem)
            .where(SourceSystem.system_name == system_name)
        ).scalar_one_or_none()

        if source:
            return source.source_system_id

        source = SourceSystem(system_name=system_name)
        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)
        return source.source_system_id

    def get_alarms(
        self,
        start_time=None,
        end_time=None,
        severity=None,
        tag=None,
        limit=50,
        offset=0
    ) -> Tuple[list, int]:

        query = (
            self.db.query(
                AlarmEvent,
                AlarmSeverity.severity_level,
                SourceSystem.system_name
            )
            .join(AlarmSeverity)
            .join(SourceSystem)
        )

        filters = []

        if start_time:
            filters.append(AlarmEvent.event_time >= start_time)
        if end_time:
            filters.append(AlarmEvent.event_time <= end_time)
        if severity:
            filters.append(AlarmSeverity.severity_level == severity)
        if tag:
            filters.append(AlarmEvent.tag == tag)

        if filters:
            query = query.filter(and_(*filters))

        total = query.count()

        records = (
            query
            .order_by(AlarmEvent.event_time.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        results = []
        for alarm, severity_level, source_name in records:
            results.append({
                "id": alarm.alarm_event_id,
                "tag": alarm.tag,
                "description": alarm.description,
                "severity": severity_level,
                "status": alarm.status,
                "event_time": alarm.event_time,
                "source_system": source_name,
                "created_at": alarm.created_at
            })

        return results, total
    
    def get_top_tags(
        self,
        start_time=None,
        end_time=None,
        limit=10
    ):
        query = (
            self.db.query(
                AlarmEvent.tag,
                func.count(AlarmEvent.alarm_event_id).label("total_events")
            )
        )

        if start_time:
            query = query.filter(AlarmEvent.event_time >= start_time)
        if end_time:
            query = query.filter(AlarmEvent.event_time <= end_time)

        results = (
            query
            .group_by(AlarmEvent.tag)
            .order_by(func.count(AlarmEvent.alarm_event_id).desc())
            .limit(limit)
            .all()
        )

        return [
            {"tag": tag, "total_events": total}
            for tag, total in results
        ]

    def bulk_insert(
        self,
        alarms: List[Dict],
        raw_payload_path: str
    ) -> Tuple[int, int]:
        """
        Inserta eventos de alarma de forma masiva.

        Retorna:
            (inserted_count, failed_count)
        """

        severity_map = self._get_severity_map()

        objects = []
        failed = 0

        try:
            for alarm in alarms:
                try:
                    severity_level = alarm["severity_level"]
                    severity_id = severity_map.get(severity_level)

                    if severity_id is None:
                        raise ValueError(f"Severity no encontrada: {severity_level}")

                    source_id = self._get_source_system_id(alarm["source_system"])

                    obj = AlarmEvent(
                        tag=alarm["tag"],
                        description=alarm.get("description"),
                        severity_id=severity_id,
                        source_system_id=source_id,
                        event_time=alarm["event_time"],
                        cleared_time=alarm.get("cleared_time"),
                        status=alarm["status"],
                        raw_payload_path=raw_payload_path,
                        created_at=datetime.now(timezone.utc),
                    )

                    objects.append(obj)

                except Exception as e:
                    failed += 1
                    logger.warning(
                        f"[SKIPPED] Alarm inválida: {alarm} | Error: {str(e)}"
                    )

            if not objects:
                logger.warning("No hay registros válidos para insertar.")
                return 0, failed

            self.db.bulk_save_objects(objects)
            self.db.commit()

            logger.info(
                f"Bulk insert completado | Insertados: {len(objects)} | Fallidos: {failed}"
            )

            return len(objects), failed

        except SQLAlchemyError as db_error:
            self.db.rollback()
            logger.error(
                f"[DB ERROR] Fallo en bulk insert: {str(db_error)}",
                exc_info=True
            )
            raise

        except Exception as e:
            self.db.rollback()
            logger.error(
                f"[UNEXPECTED ERROR] {str(e)}",
                exc_info=True
            )
            raise

        finally:
            self.db.close()

    def close(self):
        self.db.close()