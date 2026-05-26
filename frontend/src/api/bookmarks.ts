import { apiClient } from "@/api/client";
import type { BookmarkDto, BookmarkPayload } from "@/api/types";

export async function upsertBookmark(jobId: number, payload: BookmarkPayload): Promise<BookmarkDto> {
  return apiClient.put<BookmarkDto>(`/job-listings/${jobId}/bookmark`, payload);
}
