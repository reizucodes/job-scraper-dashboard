import { defineStore } from "pinia";

import { fetchJobListings } from "@/api/jobs";
import type { ApiStatus, JobListingDto, JobListingFilters } from "@/api/types";

export const useJobsStore = defineStore("jobs", {
  state: () => ({
    items: [] as JobListingDto[],
    status: "idle" as ApiStatus,
    error: "",
    filters: {
      title_query: "",
      location: "",
      work_mode: "",
      limit: 50,
      offset: 0,
    } as JobListingFilters,
  }),
  actions: {
    async load(): Promise<void> {
      this.status = "loading";
      this.error = "";
      try {
        const response = await fetchJobListings(this.filters);
        this.items = response.items;
        this.status = "success";
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to load listings";
      }
    },
    setFilters(partial: Partial<JobListingFilters>): void {
      this.filters = { ...this.filters, ...partial };
    },
  },
});
