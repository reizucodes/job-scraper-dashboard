import { defineStore } from "pinia";

import { createJobSource, deleteJobSource, fetchJobSources, updateJobSource } from "@/api/jobSources";
import { ApiError } from "@/api/client";
import type { ApiStatus, JobSourceCreatePayload, JobSourceDto, JobSourceUpdatePayload } from "@/api/types";

export const useJobSourcesStore = defineStore("jobSources", {
  state: () => ({
    items: [] as JobSourceDto[],
    status: "idle" as ApiStatus,
    error: "",
  }),
  actions: {
    async load(): Promise<void> {
      this.status = "loading";
      this.error = "";
      try {
        this.items = await fetchJobSources();
        this.status = "success";
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to load sources";
      }
    },
    async create(payload: JobSourceCreatePayload): Promise<void> {
      this.error = "";
      try {
        await createJobSource(payload);
        await this.load();
      } catch (error) {
        this.error = toSourceErrorMessage(error);
        throw error;
      }
    },
    async update(id: number, payload: JobSourceUpdatePayload): Promise<void> {
      this.error = "";
      try {
        await updateJobSource(id, payload);
        await this.load();
      } catch (error) {
        this.error = toSourceErrorMessage(error);
        throw error;
      }
    },
    async remove(id: number): Promise<void> {
      await deleteJobSource(id);
      await this.load();
    },
  },
});

function toSourceErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    const parsed = tryParseValidationError(error.message);
    if (parsed) return parsed;
    if (error instanceof ApiError) return error.message;
    return error.message;
  }
  return "Request failed";
}

function tryParseValidationError(message: string): string | null {
  try {
    const parsed = JSON.parse(message) as { detail?: string; errors?: string[] };
    if (Array.isArray(parsed.errors) && parsed.errors.length > 0) {
      return parsed.errors.join("; ");
    }
    if (typeof parsed.detail === "string" && parsed.detail.length > 0) {
      return parsed.detail;
    }
    return null;
  } catch {
    return null;
  }
}
