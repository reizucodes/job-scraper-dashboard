import { apiClient } from "@/api/client";
import type { SourceProfileDto } from "@/api/types";

export async function fetchSourceProfiles(): Promise<SourceProfileDto[]> {
  return apiClient.get<SourceProfileDto[]>("/source-profiles");
}
