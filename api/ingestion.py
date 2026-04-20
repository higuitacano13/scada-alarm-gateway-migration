from typing import Literal
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from datetime import datetime, timezone
from ingestion.generator import generate_alarm_dataset
from core.config import settings
from ingestion.loader import load_alarm_dataset
import shutil

router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"]
)

@router.post("/generate-dataset")
def generate_dataset(
    size: int = Query(1000, ge=1, le=100_000),
    file_format: Literal["json", "csv"] = Query("json")
):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    filename = f"alarms_generated_{timestamp}.{file_format}"
    path: Path = settings.dataset_generated_path / filename

    generate_alarm_dataset(
        path=path,
        size=size,
        file_format=file_format
    )

    return FileResponse(
        path=path,
        filename=filename,
        media_type=(
            "application/json"
            if file_format == "json"
            else "text/csv"
        )
    )


@router.post("/load-dataset")
def load_dataset(
    file: UploadFile = File(...)
):
    if not file.filename.endswith((".json", ".csv")):
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Solo .json o .csv"
        )

    destination = settings.dataset_processed_path / file.filename
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = load_alarm_dataset(destination)

    return {
        "message": "Dataset procesado",
        "file": file.filename,
        **result
    }

