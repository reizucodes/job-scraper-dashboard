from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RawJob(Base):
    __tablename__ = "raw_jobs"
    __table_args__ = (
        Index("ix_raw_jobs_source_scraped", "source_id", "scraped_at"),
        Index("ix_raw_jobs_external_ref", "external_ref"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("job_sources.id"), nullable=False, index=True)
    scrape_run_id: Mapped[int] = mapped_column(ForeignKey("scrape_runs.id"), nullable=False, index=True)
    external_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    scraped_at: Mapped[datetime] = mapped_column(nullable=False)
