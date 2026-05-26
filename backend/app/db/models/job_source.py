from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class JobSource(Base, TimestampMixin):
    __tablename__ = "job_sources"
    __table_args__ = (
        Index("ix_job_sources_profile_enabled", "profile_id", "enabled"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    profile_id: Mapped[int] = mapped_column(ForeignKey("source_profiles.id"), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    config: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)

    profile = relationship("SourceProfile")
