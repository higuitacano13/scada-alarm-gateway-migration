import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from dependencies.alarm_dependencies import get_alarm_service

@pytest.fixture
def client():
    mock_service = MagicMock()

    app.dependency_overrides[get_alarm_service] = lambda: mock_service

    with TestClient(app) as c:
        yield c, mock_service

    app.dependency_overrides.clear()

@patch("api.ingestion.generate_alarm_dataset")
def test_generate_dataset(mock_generate, client):
    client, _ = client

    response = client.post("/api/v1/ingestion/generate-dataset?size=10&file_format=json")

    assert response.status_code == 200

    data = response.json()
    assert data["records"] == 10
    assert data["format"] == "json"

    mock_generate.assert_called_once()

def test_generate_dataset_invalid_format(client):
    client, _ = client

    response = client.post("/ingestion/generate-dataset?file_format=xml")

    assert response.status_code == 404

@patch("api.ingestion.load_alarm_dataset")
def test_load_dataset_success(mock_loader, client, tmp_path):
    client, _ = client

    mock_loader.return_value = {
        "inserted": 10,
        "failed_db": 0,
        "invalid": 0,
        "total": 10
    }

    file_content = b'[{"tag": "PUMP_01"}]'

    response = client.post(
        "/api/v1/ingestion/load-dataset",
        files={"file": ("test.json", file_content, "application/json")}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["inserted"] == 10

def test_load_dataset_invalid_format(client):
    client, _ = client

    response = client.post(
        "/api/v1/ingestion/load-dataset",
        files={"file": ("test.txt", b"data", "text/plain")}
    )

    assert response.status_code == 400