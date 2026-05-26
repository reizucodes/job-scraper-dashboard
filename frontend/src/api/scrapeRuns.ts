import { apiClient } from "@/api/client";
import type { ScrapeRunDto, ScrapeRunTriggerResponse } from "@/api/types";

export async function triggerScrapeRun(sourceIds?: number[]): Promise<ScrapeRunTriggerResponse> {
  return apiClient.post<ScrapeRunTriggerResponse>("/scrape-runs", { source_ids: sourceIds });
}

export async function fetchScrapeRuns(limit = 50): Promise<ScrapeRunDto[]> {
  return apiClient.get<ScrapeRunDto[]>("/scrape-runs", { limit });
}
