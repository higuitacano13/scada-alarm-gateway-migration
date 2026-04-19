from fastapi import FastAPI
from api.alarms import router as alarms_router
from api.metrics import router as metrics_router
from api.ingestion import router as ingestion_router

app = FastAPI(
    title="SCADA Alarm Gateway API",
    description="API para gestión y migración de alarmas SCADA",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


app.include_router(alarms_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(ingestion_router, prefix="/api/v1")
