import { apiClient } from "@/api/client";
import type { ExportPayload } from "@/api/types";

export async function exportJobs(payload: ExportPayload): Promise<{ blob: Blob; filename: string }> {
  const { blob, contentDisposition } = await apiClient.postBlob("/exports", payload);
  const filename = contentDisposition?.match(/filename="([^"]+)"/)?.[1] ?? `job-export.${payload.format}`;
  return { blob, filename };
}
