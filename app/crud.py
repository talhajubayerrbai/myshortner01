import random
import string
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Link


def _generate_code(length: int = settings.CODE_LENGTH) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def create_link(db: Session, original_url: str, custom_code: Optional[str] = None) -> Link:
    if custom_code:
        code = custom_code
        existing = db.query(Link).filter(Link.short_code == code).first()
        if existing:
            raise ValueError(f"Custom code '{code}' is already taken.")
    else:
        code = _generate_code()
        # Retry on collision (astronomically rare, but handled)
        attempts = 0
        while db.query(Link).filter(Link.short_code == code).first():
            code = _generate_code()
            attempts += 1
            if attempts > 10:
                raise RuntimeError("Failed to generate a unique short code.")

    link = Link(short_code=code, original_url=str(original_url))
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_link_by_code(db: Session, code: str) -> Optional[Link]:
    return db.query(Link).filter(Link.short_code == code).first()


def increment_clicks(db: Session, link: Link) -> Link:
    link.click_count += 1
    db.commit()
    db.refresh(link)
    return link


def get_stats(db: Session, code: str) -> Optional[Link]:
    return db.query(Link).filter(Link.short_code == code).first()
