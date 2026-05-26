import { apiClient } from "@/api/client";
import type { JobListingFilters, JobListingListResponse } from "@/api/types";

export async function fetchJobListings(filters: JobListingFilters): Promise<JobListingListResponse> {
  const query: Record<string, unknown> = { ...filters };
  return apiClient.get<JobListingListResponse>("/job-listings", query);
}
