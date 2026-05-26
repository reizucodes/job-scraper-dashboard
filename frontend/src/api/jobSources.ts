import { apiClient } from "@/api/client";
import type { JobSourceCreatePayload, JobSourceDto, JobSourceUpdatePayload } from "@/api/types";

export async function fetchJobSources(): Promise<JobSourceDto[]> {
  return apiClient.get<JobSourceDto[]>("/job-sources");
}

export async function createJobSource(payload: JobSourceCreatePayload): Promise<JobSourceDto> {
  return apiClient.post<JobSourceDto>("/job-sources", payload);
}

export async function updateJobSource(id: number, payload: JobSourceUpdatePayload): Promise<JobSourceDto> {
  return apiClient.patch<JobSourceDto>(`/job-sources/${id}`, payload);
}

export async function deleteJobSource(id: number): Promise<void> {
  await apiClient.delete(`/job-sources/${id}`);
}
