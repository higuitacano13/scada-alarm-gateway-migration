import pytest
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

def test_top_tags_success(client):
    client, mock_service = client

    mock_service.top_tags.return_value = {
        "data": [
            {"tag": "PUMP_01", "total_events": 10}
        ]
    }

    response = client.get("/api/v1/metrics/top-tags")

    assert response.status_code == 200

    data = response.json()
    assert data["data"][0]["tag"] == "PUMP_01"

def test_top_tags_error(client):
    client, mock_service = client

    mock_service.top_tags.side_effect = ValueError("Error interno")

    response = client.get("/api/v1/metrics/top-tags")

    assert response.status_code == 500