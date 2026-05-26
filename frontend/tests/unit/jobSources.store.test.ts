import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { ApiError } from "@/api/client";
import { useJobSourcesStore } from "@/stores/jobSources";

let createFailure: Error | null = null;

vi.mock("@/api/jobSources", () => ({
  fetchJobSources: vi.fn(async () => [{
    id: 1,
    name: "Source A",
    base_url: "https://jobs.example.com",
    profile_id: 1,
    enabled: true,
    config: {},
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
  }]),
  createJobSource: vi.fn(async () => {
    if (createFailure) throw createFailure;
    return {};
  }),
  updateJobSource: vi.fn(async () => ({})),
  deleteJobSource: vi.fn(async () => undefined),
}));

describe("jobSources store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    createFailure = null;
  });

  it("create calls api and refreshes list", async () => {
    const api = await import("@/api/jobSources");
    const store = useJobSourcesStore();
    await store.create({ name: "Source A", base_url: "https://jobs.example.com", profile_id: 1, enabled: true, config: {} });
    expect(api.createJobSource).toHaveBeenCalledTimes(1);
    expect(api.fetchJobSources).toHaveBeenCalledTimes(1);
    expect(store.items).toHaveLength(1);
  });

  it("sends fixture mode config on create", async () => {
    const api = await import("@/api/jobSources");
    const store = useJobSourcesStore();
    await store.create({
      name: "Fixture Source",
      base_url: "https://jobs.example.com",
      profile_id: 1,
      enabled: true,
      config: { mode: "fixture", fixtures: [{ id: "job-1" }] },
    });

    expect(api.createJobSource).toHaveBeenCalledWith(
      expect.objectContaining({
        config: { mode: "fixture", fixtures: [{ id: "job-1" }] },
      }),
    );
  });

  it("sends live mode config on create", async () => {
    const api = await import("@/api/jobSources");
    const store = useJobSourcesStore();
    await store.create({
      name: "Live Source",
      base_url: "https://boards.greenhouse.io/acme",
      profile_id: 1,
      enabled: true,
      config: {
        mode: "live",
        jobs_url: "https://boards-api.greenhouse.io/v1/boards/acme/jobs",
        user_agent: "job-scraper-dashboard/1.0",
        timeout_seconds: 10,
      },
    });

    expect(api.createJobSource).toHaveBeenCalledWith(
      expect.objectContaining({
        config: expect.objectContaining({
          mode: "live",
          jobs_url: "https://boards-api.greenhouse.io/v1/boards/acme/jobs",
          timeout_seconds: 10,
        }),
      }),
    );
  });

  it("surfaces backend 422 validation errors", async () => {
    createFailure = new ApiError(
      422,
      JSON.stringify({ detail: "Invalid job source config", errors: ["config.jobs_url is required for live mode"] }),
    );
    const store = useJobSourcesStore();

    await expect(
      store.create({
        name: "Bad Source",
        base_url: "https://jobs.example.com",
        profile_id: 1,
        enabled: true,
        config: { mode: "live" },
      }),
    ).rejects.toBeInstanceOf(ApiError);
    expect(store.error).toContain("config.jobs_url is required for live mode");
  });

  it("updates source with edited config", async () => {
    const api = await import("@/api/jobSources");
    const store = useJobSourcesStore();
    await store.update(1, {
      name: "Updated Source",
      config: {
        mode: "live",
        jobs_url: "https://api.lever.co/v0/postings/acme?mode=json",
        timeout_seconds: 12,
      },
    });

    expect(api.updateJobSource).toHaveBeenCalledWith(
      1,
      expect.objectContaining({
        config: expect.objectContaining({
          mode: "live",
          jobs_url: "https://api.lever.co/v0/postings/acme?mode=json",
          timeout_seconds: 12,
        }),
      }),
    );
  });
});
