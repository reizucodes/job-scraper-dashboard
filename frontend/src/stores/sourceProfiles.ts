import { defineStore } from "pinia";

import { fetchSourceProfiles } from "@/api/sourceProfiles";
import type { ApiStatus, SourceProfileDto } from "@/api/types";

export const useSourceProfilesStore = defineStore("sourceProfiles", {
  state: () => ({
    items: [] as SourceProfileDto[],
    status: "idle" as ApiStatus,
    error: "",
  }),
  actions: {
    async load(): Promise<void> {
      this.status = "loading";
      this.error = "";
      try {
        this.items = await fetchSourceProfiles();
        this.status = "success";
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to load source profiles";
      }
    },
  },
});
