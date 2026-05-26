# Data Flow

This document traces implemented runtime flows across browser, frontend, backend, and database.

## A. Create Job Source
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as SourcesView.vue
  participant S as jobSources store
  participant A as api/jobSources.ts
  participant C as ApiClient
  participant R as FastAPI /job-sources router
  participant SV as JobSourceService
  participant RP as SourceProfileRepo + JobSourceRepo
  participant DB as SQLite

  B->>V: Submit source form
  V->>S: create(payload)
  S->>A: createJobSource(payload)
  A->>C: post('/job-sources', payload)
  C->>R: HTTP POST
  R->>SV: create(payload)
  SV->>RP: get(profile_id) + create(source)
  RP->>DB: SELECT + INSERT
  DB-->>RP: rows
  RP-->>SV: created source
  SV-->>R: domain entity
  R-->>C: JobSourceResponse JSON
  C-->>S: parsed DTO
  S->>S: load() refresh list
  S-->>V: updated items/status
```

## B. Run Scrape
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as RunsView.vue
  participant S as scrapeRuns store
  participant A as api/scrapeRuns.ts
  participant C as ApiClient
  participant R as /scrape-runs router
  participant SV as ScrapeRunService
  participant DB as SQLite

  B->>V: Trigger scrape run
  V->>S: trigger(sourceIds?)
  S->>A: triggerScrapeRun(sourceIds)
  A->>C: post('/scrape-runs', {source_ids})
  C->>R: HTTP POST
  R->>SV: trigger_run(source_ids)
  SV->>DB: create scrape_run(status=running)
  SV->>SV: resolve sources + validate missing/disabled IDs
  SV->>SV: scrape + persist + normalize + dedupe
  SV->>DB: update scrape_run metrics/status
  R-->>C: ScrapeRunTriggerResponse
  C-->>S: trigger result
  S->>A: fetchScrapeRuns(50)
  A->>C: get('/scrape-runs')
  C->>R: HTTP GET
  R-->>C: run list
  C-->>S: runs
  S-->>V: render run summary + table
```

## C. Third-Party API Fetch
File path focus:
- `backend/app/scrapers/profiles/greenhouse_adapter.py`
- `backend/app/scrapers/profiles/lever_adapter.py`

Flow:
1. `ScrapeRunService` resolves source profile.
2. `ScraperRegistry` resolves adapter by profile code.
3. Adapter chooses `mode` (`fixture` or `live`).
4. In live mode, adapter uses `httpx.Client(...).get(jobs_url)`.
5. Adapter validates response shape and emits `ScrapedRecord[]`.

## D. RawJob Persistence
File:
- `backend/app/services/scrape_run_service.py`
- `backend/app/repositories/raw_job_repo.py`

Flow:
1. For each `ScrapedRecord`, service computes `payload_hash`.
2. Service creates `RawJob` via `SQLAlchemyRawJobRepository.create`.
3. `raw_jobs` row captures provider payload and scrape timestamp.

## E. Normalization
File:
- `backend/app/services/normalization_service.py`

Flow:
1. Service reads profile-specific preferred keys for title/company.
2. Reads location/work mode from multiple candidate fields.
3. Normalizes posted datetime and string lists.
4. Produces `NormalizedJobData`.

## F. Dedupe / Upsert
File:
- `backend/app/services/dedupe_service.py`

Flow:
1. Generate canonical key priority:
   - external ref
   - apply URL
   - fallback hash(title/company/location)
2. Look up existing listing by canonical key.
3. Insert new listing or update mutable fields + `last_seen_at`.
4. Return action: `inserted`, `updated`, or `duplicate`.

## G. Job Listing Display
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as JobsView.vue
  participant S as jobs store
  participant A as api/jobs.ts
  participant C as ApiClient
  participant R as /job-listings router
  participant SV as JobListingService
  participant RP as ListingRepo + BookmarkRepo
  participant DB as SQLite

  B->>V: Apply filters
  V->>S: setFilters + load()
  S->>A: fetchJobListings(filters)
  A->>C: get('/job-listings', query)
  C->>R: HTTP GET
  R->>SV: list_listings(...)
  SV->>RP: list_filtered + list_by_job_ids
  RP->>DB: SELECT listings + bookmarks
  DB-->>RP: rows
  RP-->>SV: entities
  SV-->>R: items + bookmark_status_by_listing_id
  R-->>C: JobListingListResponse
  C-->>S: DTO list
  S-->>V: render table with bookmark_status
```

## H. Bookmark Update
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as JobsView.vue
  participant BS as bookmarks store
  participant A as api/bookmarks.ts
  participant C as ApiClient
  participant R as /job-listings/{id}/bookmark router
  participant SV as JobBookmarkService
  participant RP as ListingRepo + BookmarkRepo
  participant DB as SQLite

  B->>V: Change bookmark select
  V->>BS: setStatus(jobId, status)
  BS->>A: upsertBookmark(jobId, payload)
  A->>C: put('/job-listings/{id}/bookmark')
  C->>R: HTTP PUT
  R->>SV: upsert(listing_id, payload)
  SV->>RP: get(listing) + upsert(bookmark)
  RP->>DB: SELECT + INSERT/UPDATE
  DB-->>RP: row
  R-->>C: JobBookmarkResponse
  C-->>BS: updated status
  BS-->>V: return status
  V->>V: update local row bookmark_status
```

## I. CSV Export
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as JobsView.vue
  participant S as exports store
  participant A as api/exports.ts
  participant C as ApiClient
  participant R as /exports router
  participant SV as ExportService
  participant E as CsvExporter
  participant DB as SQLite

  B->>V: Export filtered jobs (CSV)
  V->>S: run('csv', filters)
  S->>A: exportJobs(payload)
  A->>C: postBlob('/exports', payload)
  C->>R: HTTP POST
  R->>SV: export('csv', filters)
  SV->>DB: query listings + bookmarks
  SV->>E: export(rows)
  E-->>SV: ExportArtifact(csv bytes)
  SV-->>R: artifact + filename
  R-->>C: binary response + content-disposition
  C-->>S: Blob + filename
  S->>B: trigger browser download
```

## J. XLSX Export
Same flow as CSV, but `ExporterRegistry` resolves `XlsxExporter`.

Files:
- `backend/app/exporters/registry.py`
- `backend/app/exporters/xlsx_exporter.py`

## Cross-Layer Notes
- Browser/UI bookmark value and export bookmark value are both based on persisted bookmark state.
- Selected source scrape now reports missing/disabled IDs explicitly in run failures.
