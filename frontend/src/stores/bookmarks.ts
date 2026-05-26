import { defineStore } from "pinia";

import { upsertBookmark } from "@/api/bookmarks";
import type { ApiStatus, BookmarkStatus } from "@/api/types";

export const useBookmarksStore = defineStore("bookmarks", {
  state: () => ({
    status: "idle" as ApiStatus,
    error: "",
  }),
  actions: {
    async setStatus(jobId: number, status: BookmarkStatus): Promise<BookmarkStatus> {
      this.status = "loading";
      this.error = "";
      try {
        const bookmark = await upsertBookmark(jobId, { status, notes: null });
        this.status = "success";
        return bookmark.status;
      } catch (error) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Failed to update bookmark";
        throw error;
      }
    },
  },
});
