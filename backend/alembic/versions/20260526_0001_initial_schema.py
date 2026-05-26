"""initial schema

Revision ID: 20260526_0001
Revises: None
Create Date: 2026-05-26 10:00:00.000000
"""

from __future__ import annotations

from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


revision = "20260526_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_source_profiles")),
        sa.UniqueConstraint("code", name=op.f("uq_source_profiles_code")),
    )
    op.create_index(op.f("ix_source_profiles_code"), "source_profiles", ["code"], unique=False)

    op.create_table(
        "job_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.String(length=1024), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["source_profiles.id"], name=op.f("fk_job_sources_profile_id_source_profiles")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_job_sources")),
    )
    op.create_index(op.f("ix_job_sources_enabled"), "job_sources", ["enabled"], unique=False)
    op.create_index("ix_job_sources_profile_enabled", "job_sources", ["profile_id", "enabled"], unique=False)

    op.create_table(
        "scrape_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("records_seen", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_inserted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_updated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("duplicates", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failures", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["job_sources.id"], name=op.f("fk_scrape_runs_source_id_job_sources")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_scrape_runs")),
    )
    op.create_index(op.f("ix_scrape_runs_source_id"), "scrape_runs", ["source_id"], unique=False)
    op.create_index(op.f("ix_scrape_runs_status"), "scrape_runs", ["status"], unique=False)
    op.create_index("ix_scrape_runs_source_started", "scrape_runs", ["source_id", "started_at"], unique=False)

    op.create_table(
        "raw_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("scrape_run_id", sa.Integer(), nullable=False),
        sa.Column("external_ref", sa.String(length=255), nullable=True),
        sa.Column("source_snapshot", sa.Text(), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("payload_hash", sa.String(length=128), nullable=False),
        sa.Column("scraped_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["scrape_run_id"], ["scrape_runs.id"], name=op.f("fk_raw_jobs_scrape_run_id_scrape_runs")),
        sa.ForeignKeyConstraint(["source_id"], ["job_sources.id"], name=op.f("fk_raw_jobs_source_id_job_sources")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_raw_jobs")),
    )
    op.create_index(op.f("ix_raw_jobs_external_ref"), "raw_jobs", ["external_ref"], unique=False)
    op.create_index(op.f("ix_raw_jobs_payload_hash"), "raw_jobs", ["payload_hash"], unique=False)
    op.create_index(op.f("ix_raw_jobs_scrape_run_id"), "raw_jobs", ["scrape_run_id"], unique=False)
    op.create_index(op.f("ix_raw_jobs_source_id"), "raw_jobs", ["source_id"], unique=False)
    op.create_index("ix_raw_jobs_source_scraped", "raw_jobs", ["source_id", "scraped_at"], unique=False)

    op.create_table(
        "job_listings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("raw_job_id", sa.Integer(), nullable=True),
        sa.Column("canonical_key", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("work_mode", sa.String(length=32), nullable=True),
        sa.Column("employment_type", sa.String(length=64), nullable=True),
        sa.Column("posted_at", sa.DateTime(), nullable=True),
        sa.Column("apply_url", sa.String(length=1024), nullable=False),
        sa.Column("description_snippet", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["raw_job_id"], ["raw_jobs.id"], name=op.f("fk_job_listings_raw_job_id_raw_jobs")),
        sa.ForeignKeyConstraint(["source_id"], ["job_sources.id"], name=op.f("fk_job_listings_source_id_job_sources")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_job_listings")),
        sa.UniqueConstraint("canonical_key", name=op.f("uq_job_listings_canonical_key")),
    )
    op.create_index(op.f("ix_job_listings_is_active"), "job_listings", ["is_active"], unique=False)
    op.create_index(op.f("ix_job_listings_location"), "job_listings", ["location"], unique=False)
    op.create_index(op.f("ix_job_listings_raw_job_id"), "job_listings", ["raw_job_id"], unique=False)
    op.create_index(op.f("ix_job_listings_source_id"), "job_listings", ["source_id"], unique=False)
    op.create_index(op.f("ix_job_listings_title"), "job_listings", ["title"], unique=False)
    op.create_index(op.f("ix_job_listings_work_mode"), "job_listings", ["work_mode"], unique=False)
    op.create_index("ix_job_listings_company", "job_listings", ["company"], unique=False)
    op.create_index("ix_job_listings_posted", "job_listings", ["posted_at"], unique=False)
    op.create_index("ix_job_listings_source_active", "job_listings", ["source_id", "is_active"], unique=False)

    op.create_table(
        "job_bookmarks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["job_listings.id"], name=op.f("fk_job_bookmarks_job_id_job_listings")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_job_bookmarks")),
        sa.UniqueConstraint("job_id", name=op.f("uq_job_bookmarks_job_id")),
    )
    op.create_index(op.f("ix_job_bookmarks_job_id"), "job_bookmarks", ["job_id"], unique=False)
    op.create_index(op.f("ix_job_bookmarks_status"), "job_bookmarks", ["status"], unique=False)

    now = datetime.now(timezone.utc)
    source_profiles = sa.table(
        "source_profiles",
        sa.column("code", sa.String),
        sa.column("display_name", sa.String),
        sa.column("active", sa.Boolean),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )
    op.bulk_insert(
        source_profiles,
        [
            {"code": "greenhouse", "display_name": "Greenhouse", "active": True, "created_at": now, "updated_at": now},
            {"code": "lever", "display_name": "Lever", "active": True, "created_at": now, "updated_at": now},
            {"code": "custom-html", "display_name": "Custom HTML", "active": True, "created_at": now, "updated_at": now},
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_job_bookmarks_status"), table_name="job_bookmarks")
    op.drop_index(op.f("ix_job_bookmarks_job_id"), table_name="job_bookmarks")
    op.drop_table("job_bookmarks")

    op.drop_index("ix_job_listings_source_active", table_name="job_listings")
    op.drop_index("ix_job_listings_posted", table_name="job_listings")
    op.drop_index("ix_job_listings_company", table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_work_mode"), table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_title"), table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_source_id"), table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_raw_job_id"), table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_location"), table_name="job_listings")
    op.drop_index(op.f("ix_job_listings_is_active"), table_name="job_listings")
    op.drop_table("job_listings")

    op.drop_index("ix_raw_jobs_source_scraped", table_name="raw_jobs")
    op.drop_index(op.f("ix_raw_jobs_source_id"), table_name="raw_jobs")
    op.drop_index(op.f("ix_raw_jobs_scrape_run_id"), table_name="raw_jobs")
    op.drop_index(op.f("ix_raw_jobs_payload_hash"), table_name="raw_jobs")
    op.drop_index(op.f("ix_raw_jobs_external_ref"), table_name="raw_jobs")
    op.drop_table("raw_jobs")

    op.drop_index("ix_scrape_runs_source_started", table_name="scrape_runs")
    op.drop_index(op.f("ix_scrape_runs_status"), table_name="scrape_runs")
    op.drop_index(op.f("ix_scrape_runs_source_id"), table_name="scrape_runs")
    op.drop_table("scrape_runs")

    op.drop_index("ix_job_sources_profile_enabled", table_name="job_sources")
    op.drop_index(op.f("ix_job_sources_enabled"), table_name="job_sources")
    op.drop_table("job_sources")

    op.drop_index(op.f("ix_source_profiles_code"), table_name="source_profiles")
    op.drop_table("source_profiles")
