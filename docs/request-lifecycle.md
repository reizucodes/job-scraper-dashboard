# Request Lifecycle

This document shows end-to-end request handling from browser UI to SQLite and back.

## Common Path Template
```mermaid
sequenceDiagram
  participant B as Browser
  participant V as Vue View
  participant S as Pinia Store
  participant M as API Module
  participant C as ApiClient
  participant R as FastAPI Router
  participant SV as Service
  participant RP as Repository
  participant ORM as SQLAlchemy Session
  participant DB as SQLite

  B->>V: UI interaction
  V->>S: store action
  S->>M: endpoint function
  M->>C: HTTP helper call
  C->>R: HTTP request
  R->>SV: service method
  SV->>RP: repository method
  RP->>ORM: query/flush
  ORM->>DB: SQL
  DB-->>ORM: rows
  ORM-->>RP: entities
  RP-->>SV: results
  SV-->>R: domain output
  R-->>C: JSON/Binary response
  C-->>S: parsed data
  S-->>V: reactive state update
```

## Create Source Lifecycle
```mermaid
sequenceDiagram
  participant V as SourcesView.vue
  participant S as stores/jobSources.ts
  participant M as api/jobSources.ts
  participant C as api/client.ts
  participant R as routers/job_sources.py
  participant D as api/deps.py
  participant SV as services/job_source_service.py
  participant PR as repositories/source_profile_repo.py
  participant JR as repositories/job_source_repo.py
  participant DB as SQLite

  V->>S: create(payload)
  S->>M: createJobSource(payload)
  M->>C: post('/job-sources', payload)
  C->>R: POST /job-sources
  R->>D: get_job_source_service()
  D-->>R: JobSourceService
  R->>SV: create(payload)
  SV->>PR: get(profile_id)
  PR->>DB: SELECT source_profiles
  SV->>SV: validate config
  SV->>JR: create(source)
  JR->>DB: INSERT job_sources
  SV->>DB: COMMIT
  R-->>C: JobSourceResponse
  C-->>S: DTO
  S->>S: load() list refresh
```

## Run Scrape Lifecycle
```mermaid
sequenceDiagram
  participant V as RunsView.vue
  participant S as stores/scrapeRuns.ts
  participant M as api/scrapeRuns.ts
  participant C as api/client.ts
  participant R as routers/scrape_runs.py
  participant SV as services/scrape_run_service.py
  participant REG as scrapers/registry.py
  participant AD as scrapers/profiles/*
  participant RR as raw_job_repo.py
  participant DS as dedupe_service.py
  participant LR as job_listing_repo.py
  participant DB as SQLite

  V->>S: trigger(sourceIds?)
  S->>M: triggerScrapeRun(sourceIds)
  M->>C: POST /scrape-runs
  C->>R: request
  R->>SV: trigger_run(source_ids)
  SV->>DB: INSERT scrape_runs(status=running)
  SV->>SV: resolve selected IDs; mark missing/disabled failures
  loop each resolved enabled source
    SV->>REG: get(profile_code)
    REG-->>SV: adapter
    SV->>AD: scrape(source)
    AD-->>SV: ScrapedRecord[]
    loop each record
      SV->>RR: create(raw_job)
      RR->>DB: INSERT raw_jobs
      SV->>DS: normalize + canonical key + upsert
      DS->>LR: select/create/update listing
      LR->>DB: SELECT/INSERT/UPDATE job_listings
    end
  end
  SV->>DB: UPDATE scrape_runs(metrics,status)
  R-->>C: ScrapeRunTriggerResponse
  C-->>S: trigger result
  S->>M: fetchScrapeRuns
  M->>C: GET /scrape-runs
  C-->>S: runs
```

## Bookmark Update Lifecycle
```mermaid
sequenceDiagram
  participant V as JobsView.vue
  participant BS as stores/bookmarks.ts
  participant BM as api/bookmarks.ts
  participant C as api/client.ts
  participant R as routers/bookmarks.py
  participant SV as services/job_bookmark_service.py
  participant LR as job_listing_repo.py
  participant BR as job_bookmark_repo.py
  participant DB as SQLite

  V->>BS: setStatus(jobId,status)
  BS->>BM: upsertBookmark(jobId,payload)
  BM->>C: PUT /job-listings/{id}/bookmark
  C->>R: request
  R->>SV: upsert(listing_id,payload)
  SV->>LR: get(listing)
  LR->>DB: SELECT job_listings
  SV->>BR: upsert(bookmark)
  BR->>DB: INSERT/UPDATE job_bookmarks
  SV->>DB: COMMIT
  R-->>C: JobBookmarkResponse
  C-->>BS: updated bookmark status
  BS-->>V: status return
  V->>V: update row.bookmark_status
```

## Export Lifecycle
```mermaid
sequenceDiagram
  participant V as JobsView.vue
  participant ES as stores/exports.ts
  participant EM as api/exports.ts
  participant C as api/client.ts
  participant R as routers/exports.py
  participant SV as services/export_service.py
  participant LR as job_listing_repo.py
  participant BR as job_bookmark_repo.py
  participant REG as exporters/registry.py
  participant EX as csv_exporter.py/xlsx_exporter.py
  participant DB as SQLite

  V->>ES: run(format,filters)
  ES->>EM: exportJobs(payload)
  EM->>C: postBlob('/exports')
  C->>R: request
  R->>SV: export(format,filters)
  SV->>LR: list_filtered(filters)
  LR->>DB: SELECT job_listings
  SV->>BR: list_by_job_ids(ids)
  BR->>DB: SELECT job_bookmarks
  SV->>REG: resolve(format)
  REG-->>SV: exporter
  SV->>EX: export(rows)
  EX-->>SV: bytes/media type/ext
  R-->>C: binary response + filename header
  C-->>ES: blob + filename
  ES->>V: browser download trigger
```

## Laravel Concept Mapping for Lifecycle
- Vue View + Store + API module ~= Blade/SPA UI + client service abstraction.
- FastAPI Router ~= Laravel Controller action.
- Service layer ~= Laravel Service class.
- Repository layer ~= Laravel Repository pattern.
- SQLAlchemy session/model ~= Eloquent/Query Builder execution path.
