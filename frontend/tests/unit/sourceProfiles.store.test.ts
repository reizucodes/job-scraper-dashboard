import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useSourceProfilesStore } from "@/stores/sourceProfiles";

vi.mock("@/api/sourceProfiles", () => ({
  fetchSourceProfiles: vi.fn(async () => [{ id: 1, code: "greenhouse", display_name: "Greenhouse", active: true }]),
}));

describe("sourceProfiles store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("loads profiles", async () => {
    const store = useSourceProfilesStore();
    await store.load();
    expect(store.items).toHaveLength(1);
    expect(store.items[0].code).toBe("greenhouse");
    expect(store.status).toBe("success");
  });
});
