from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func

from api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)