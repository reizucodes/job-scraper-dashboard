import { describe, expect, it, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";

import RunsView from "@/views/RunsView.vue";

vi.mock("@/api/jobSources", () => ({
  fetchJobSources: vi.fn(async () => [
    {
      id: 1,
      name: "Source A",
      base_url: "https://jobs.example.com",
      profile_id: 1,
      enabled: true,
      config: {},
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-01T00:00:00Z",
    },
  ]),
  createJobSource: vi.fn(),
  updateJobSource: vi.fn(),
  deleteJobSource: vi.fn(),
}));
vi.mock("@/api/scrapeRuns", () => ({
  fetchScrapeRuns: vi.fn(async () => []),
  triggerScrapeRun: vi.fn(async () => ({
    run_id: 10,
    status: "completed",
    metrics: { records_seen: 2, records_inserted: 1, records_updated: 0, duplicates: 1, failures: 0, duration_ms: 10 },
  })),
}));

describe("RunsView integration", () => {
  it("loads runs and triggers scrape", async () => {
    const sourceApi = await import("@/api/jobSources");
    const runsApi = await import("@/api/scrapeRuns");

    const wrapper = mount(RunsView, { global: { plugins: [createPinia()] } });
    await Promise.resolve();
    await Promise.resolve();

    const triggerButton = wrapper.find("button");
    await triggerButton.trigger("click");

    expect(sourceApi.fetchJobSources).toHaveBeenCalled();
    expect(runsApi.fetchScrapeRuns).toHaveBeenCalled();
    expect(runsApi.triggerScrapeRun).toHaveBeenCalled();
    expect(wrapper.text()).toContain("Run #10 completed");
  });
});
