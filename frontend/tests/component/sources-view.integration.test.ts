import { describe, expect, it, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia } from "pinia";

import SourcesView from "@/views/SourcesView.vue";

const profileRows = [
  { id: 1, code: "greenhouse", display_name: "Greenhouse", active: true },
  { id: 2, code: "lever", display_name: "Lever", active: true },
];

let sourceRows: Array<Record<string, unknown>> = [];

vi.mock("@/api/sourceProfiles", () => ({
  fetchSourceProfiles: vi.fn(async () => profileRows),
}));

vi.mock("@/api/jobSources", () => ({
  fetchJobSources: vi.fn(async () => sourceRows),
  createJobSource: vi.fn(async () => ({})),
  updateJobSource: vi.fn(async () => ({})),
  deleteJobSource: vi.fn(async () => undefined),
}));

describe("SourcesView integration", () => {
  it("shows fixture JSON parse error for invalid input", async () => {
    sourceRows = [];
    const wrapper = mount(SourcesView, { global: { plugins: [createPinia()] } });
    await flushPromises();
    await wrapper.find("#source-fixtures-json").setValue("not-json");
    expect(wrapper.text()).toContain("Fixture JSON must be valid JSON");
  });

  it("hydrates edit form from existing source config", async () => {
    sourceRows = [
      {
        id: 7,
        name: "Lever Live",
        base_url: "https://api.lever.co",
        profile_id: 2,
        enabled: true,
        config: {
          mode: "live",
          jobs_url: "https://api.lever.co/v0/postings/acme?mode=json",
          user_agent: "ua-x",
          timeout_seconds: 8,
        },
        created_at: "2026-01-01T00:00:00Z",
        updated_at: "2026-01-01T00:00:00Z",
      },
    ];
    const wrapper = mount(SourcesView, { global: { plugins: [createPinia()] } });
    await flushPromises();

    const editButton = wrapper.findAll("button").find((node) => node.text().trim() === "Edit");
    expect(editButton).toBeTruthy();
    await editButton!.trigger("click");

    expect((wrapper.find("#source-config-mode").element as HTMLSelectElement).value).toBe("live");
    expect((wrapper.find("#source-jobs-url").element as HTMLInputElement).value).toBe(
      "https://api.lever.co/v0/postings/acme?mode=json",
    );
    expect((wrapper.find("#source-user-agent").element as HTMLInputElement).value).toBe("ua-x");
    expect((wrapper.find("#source-timeout").element as HTMLInputElement).value).toBe("8");
  });
});
