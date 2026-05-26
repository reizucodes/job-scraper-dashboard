from app.db import models


def test_expected_tables_present() -> None:
    table_names = set(models.SourceProfile.metadata.tables.keys())

    assert "source_profiles" in table_names
    assert "job_sources" in table_names
    assert "scrape_runs" in table_names
    assert "raw_jobs" in table_names
    assert "job_listings" in table_names
    assert "job_bookmarks" in table_names


def test_job_listing_has_canonical_key_unique_constraint() -> None:
    table = models.JobListing.__table__
    unique_columns = {
        tuple(col.name for col in constraint.columns)
        for constraint in table.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    assert ("canonical_key",) in unique_columns
