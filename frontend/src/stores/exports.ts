import { defineStore } from "pinia";

import { exportJobs } from "@/api/exports";
import type { ApiStatus, ExportFormat, JobListingFilters } from "@/api/types";

export const useExportsStore = defineStore("exports", {
  state: () => ({
    status: "idle" as ApiStatus,
    error: "",
    lastFilename: "",
  }),
  actions: {
    async run(format: ExportFormat, filters: JobListingFilters): Promise<void> {
      this.status = "loading";
      this.error = "";
      try {
        const { blob, filename } = await exportJobs({ format, filters });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        this.lastFilename = filename;
        this.status = "success";
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to export";
      }
    },
  },
});
