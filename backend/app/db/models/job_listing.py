from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobListing(Base):
    __tablename__ = "job_listings"
    __table_args__ = (
        Index("ix_job_listings_source_active", "source_id", "is_active"),
        Index("ix_job_listings_company", "company"),
        Index("ix_job_listings_posted", "posted_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("job_sources.id"), nullable=False, index=True)
    raw_job_id: Mapped[int | None] = mapped_column(ForeignKey("raw_jobs.id"), nullable=True, index=True)
    canonical_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    work_mode: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    employment_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    apply_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    description_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
