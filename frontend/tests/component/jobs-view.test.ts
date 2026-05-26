import { describe, expect, it, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";

import JobsView from "@/views/JobsView.vue";

vi.mock("@/api/jobs", () => ({
  fetchJobListings: vi.fn(async () => ({
    items: [
      {
        id: 1,
        source_id: 1,
        raw_job_id: null,
        canonical_key: "k1",
        title: "Python Engineer",
        company: "Acme",
        location: "Remote",
        work_mode: "remote",
        posted_at: null,
        apply_url: "https://jobs.example.com/1",
        description_snippet: "Build APIs",
        tags: ["backend"],
        skills: ["Python"],
        first_seen_at: "2026-01-01T00:00:00Z",
        last_seen_at: "2026-01-01T00:00:00Z",
        is_active: true,
        bookmark_status: "interested",
      },
    ],
    limit: 50,
    offset: 0,
  })),
}));
vi.mock("@/api/bookmarks", () => ({
  upsertBookmark: vi.fn(async () => ({ id: 1, job_id: 1, status: "applied", notes: null, updated_at: "2026-01-01T00:00:00Z" })),
}));
vi.mock("@/api/exports", () => ({
  exportJobs: vi.fn(async () => ({ blob: new Blob(["x"]), filename: "job-export.csv" })),
}));

describe("JobsView integration", () => {
  it("filters, bookmarks, and exports", async () => {
    const jobsApi = await import("@/api/jobs");
    const bookmarkApi = await import("@/api/bookmarks");
    const exportApi = await import("@/api/exports");

    const wrapper = mount(JobsView, { global: { plugins: [createPinia()] } });
    await Promise.resolve();
    await Promise.resolve();

    await wrapper.find("input[placeholder='Title filter']").setValue("Python");
    await wrapper.find("[data-testid='apply-filters']").trigger("click");
    expect(jobsApi.fetchJobListings).toHaveBeenCalled();
    expect(wrapper.find("a[href='https://jobs.example.com/1']").exists()).toBe(true);
    expect((wrapper.find("[data-testid='bookmark-select']").element as HTMLSelectElement).value).toBe("interested");

    await wrapper.find("[data-testid='bookmark-select']").setValue("applied");
    expect(bookmarkApi.upsertBookmark).toHaveBeenCalled();
    expect((wrapper.find("[data-testid='bookmark-select']").element as HTMLSelectElement).value).toBe("applied");

    await wrapper.find("[data-testid='run-export']").trigger("click");
    expect(exportApi.exportJobs).toHaveBeenCalled();
  });
});
