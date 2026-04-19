from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = (
    f"mssql+pyodbc://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_server}/{settings.db_name}"
    f"?driver={settings.db_driver.replace(' ', '+')}"
    "&TrustServerCertificate=yes"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)