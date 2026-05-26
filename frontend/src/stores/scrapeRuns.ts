import { defineStore } from "pinia";

import { fetchScrapeRuns, triggerScrapeRun } from "@/api/scrapeRuns";
import type { ApiStatus, ScrapeRunDto, ScrapeRunTriggerResponse } from "@/api/types";

export const useScrapeRunsStore = defineStore("scrapeRuns", {
  state: () => ({
    items: [] as ScrapeRunDto[],
    status: "idle" as ApiStatus,
    triggerStatus: "idle" as ApiStatus,
    lastTrigger: null as ScrapeRunTriggerResponse | null,
    error: "",
  }),
  actions: {
    async load(): Promise<void> {
      this.status = "loading";
      this.error = "";
      try {
        this.items = await fetchScrapeRuns(50);
        this.status = "success";
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to load runs";
      }
    },
    async trigger(sourceIds?: number[]): Promise<void> {
      this.triggerStatus = "loading";
      this.error = "";
      try {
        this.lastTrigger = await triggerScrapeRun(sourceIds);
        this.triggerStatus = "success";
        await this.load();
      } catch (error) {
        this.triggerStatus = "error";
        this.error = error instanceof Error ? error.message : "Failed to trigger run";
      }
    },
  },
});
