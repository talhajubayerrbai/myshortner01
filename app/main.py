from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine, get_db
from app.routers import links
from app.schemas import HealthResponse

# Create tables on startup (idempotent; Alembic handles migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A simple, fast URL shortener built with FastAPI and PostgreSQL.",
    version="1.0.0",
)

app.include_router(links.router)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health(db: Session = Depends(get_db)):
    """Liveness / readiness probe."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return HealthResponse(status="ok", db=db_status)
