export type ApiStatus = "idle" | "loading" | "success" | "error";

export type BookmarkStatus = "new" | "interested" | "applied" | "rejected";
export type ExportFormat = "csv" | "xlsx";

export interface SourceProfileDto {
  id: number;
  code: string;
  display_name: string;
  active: boolean;
}

export interface JobSourceDto {
  id: number;
  name: string;
  base_url: string;
  profile_id: number;
  enabled: boolean;
  config: JobSourceConfig;
  created_at: string;
  updated_at: string;
}

export interface JobSourceCreatePayload {
  name: string;
  base_url: string;
  profile_id: number;
  enabled: boolean;
  config: JobSourceConfig;
}

export interface JobSourceUpdatePayload {
  name?: string;
  base_url?: string;
  enabled?: boolean;
  config?: JobSourceConfig;
}

export type JobSourceConfigMode = "fixture" | "live";

export interface JobSourceConfig {
  mode?: JobSourceConfigMode;
  fixtures?: Array<Record<string, unknown>>;
  jobs_url?: string;
  user_agent?: string;
  timeout_seconds?: number;
  [key: string]: unknown;
}

export interface ScrapeRunDto {
  id: number;
  source_id: number | null;
  status: string;
  started_at: string;
  ended_at: string | null;
  duration_ms: number | null;
  records_seen: number;
  records_inserted: number;
  records_updated: number;
  duplicates: number;
  failures: number;
  error_summary: string | null;
}

export interface ScrapeRunTriggerMetrics {
  records_seen: number;
  records_inserted: number;
  records_updated: number;
  duplicates: number;
  failures: number;
  duration_ms: number;
}

export interface ScrapeRunTriggerResponse {
  run_id: number;
  status: "completed" | "failed";
  metrics: ScrapeRunTriggerMetrics;
}

export interface JobListingDto {
  id: number;
  source_id: number;
  raw_job_id: number | null;
  canonical_key: string;
  title: string;
  company: string;
  location: string | null;
  work_mode: string | null;
  posted_at: string | null;
  apply_url: string;
  description_snippet: string | null;
  tags: string[];
  skills: string[];
  first_seen_at: string;
  last_seen_at: string;
  is_active: boolean;
  bookmark_status: BookmarkStatus;
}

export interface JobListingListResponse {
  items: JobListingDto[];
  limit: number;
  offset: number;
}

export interface JobListingFilters {
  source_id?: number;
  is_active?: boolean;
  work_mode?: string;
  location?: string;
  title_query?: string;
  posted_from?: string;
  posted_to?: string;
  limit?: number;
  offset?: number;
}

export interface BookmarkPayload {
  status: BookmarkStatus;
  notes?: string | null;
}

export interface BookmarkDto {
  id: number;
  job_id: number;
  status: BookmarkStatus;
  notes: string | null;
  updated_at: string;
}

export interface ExportPayload {
  format: ExportFormat;
  filters: JobListingFilters;
}
