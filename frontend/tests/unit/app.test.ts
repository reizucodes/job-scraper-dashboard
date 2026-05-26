import { describe, expect, it } from "vitest";

import { apiClient } from "@/api/client";

describe("api client scaffold", () => {
  it("has a base url", () => {
    expect(apiClient.getBaseUrl()).toBeTypeOf("string");
  });
});
