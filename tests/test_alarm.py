import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from main import app
from dependencies.alarm_dependencies import get_alarm_service

@pytest.fixture
def client():
    mock_service = MagicMock()

    app.dependency_overrides[get_alarm_service] = lambda: mock_service

    with TestClient(app) as c:
        yield c, mock_service

    app.dependency_overrides.clear()

def test_get_alarms_success(client):
    client, mock_service = client

    mock_service.get_alarms.return_value = (
        [{
            "id": 1,
            "tag": "PUMP_01",
            "description": "Alarm triggered",
            "severity": 3,
            "status": "ACTIVE",
            "event_time": datetime.now(timezone.utc).isoformat(),
            "source_system": "SCADA_A",
            "created_at": datetime.now(timezone.utc).isoformat()
        }],
        1
    )

    response = client.get("/api/v1/alarms")

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["tag"] == "PUMP_01"

def test_get_alarms_invalid_dates(client):
    client, mock_service = client

    mock_service.get_alarms.side_effect = ValueError("Invalid date range")

    response = client.get("/api/v1/alarms")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date range"

def test_get_alarms_with_filters(client):
    client, mock_service = client

    mock_service.get_alarms.return_value = ([], 0)

    response = client.get("/api/v1/alarms?severity=3&limit=10")

    assert response.status_code == 200

    mock_service.get_alarms.assert_called_once()