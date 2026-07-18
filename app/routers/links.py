from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from app.database import get_db
from app.schemas import ShortenRequest, ShortenResponse, StatsResponse

router = APIRouter()


@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    """Create a shortened URL."""
    try:
        link = crud.create_link(db, str(payload.url), payload.custom_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    return ShortenResponse(
        short_code=link.short_code,
        short_url=f"{settings.BASE_URL}/{link.short_code}",
        original_url=link.original_url,
        created_at=link.created_at,
    )


@router.get("/{code}/stats", response_model=StatsResponse)
def get_stats(code: str, db: Session = Depends(get_db)):
    """Return click statistics for a short code."""
    link = crud.get_stats(db, code)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found.")
    return link


@router.get("/{code}")
def redirect_to_url(code: str, db: Session = Depends(get_db)):
    """Redirect to the original URL."""
    link = crud.get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found.")
    crud.increment_clicks(db, link)
    return RedirectResponse(url=link.original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
