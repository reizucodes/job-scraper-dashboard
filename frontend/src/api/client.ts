export interface ApiClientOptions {
  baseUrl: string;
}

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message);
  }
}

export class ApiClient {
  constructor(private readonly options: ApiClientOptions) {}

  getBaseUrl(): string {
    return this.options.baseUrl;
  }

  async get<T>(path: string, query?: Record<string, unknown>): Promise<T> {
    const url = new URL(`${this.options.baseUrl}${path}`);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value === undefined) continue;
        if (value === null) continue;
        url.searchParams.set(key, String(value));
      }
    }
    const response = await fetch(url.toString());
    return this.handleJson<T>(response);
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${this.options.baseUrl}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return this.handleJson<T>(response);
  }

  async patch<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${this.options.baseUrl}${path}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return this.handleJson<T>(response);
  }

  async put<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${this.options.baseUrl}${path}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return this.handleJson<T>(response);
  }

  async delete(path: string): Promise<void> {
    const response = await fetch(`${this.options.baseUrl}${path}`, { method: "DELETE" });
    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }
  }

  async postBlob(path: string, body: unknown): Promise<{ blob: Blob; contentDisposition: string | null }> {
    const response = await fetch(`${this.options.baseUrl}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }
    return {
      blob: await response.blob(),
      contentDisposition: response.headers.get("content-disposition"),
    };
  }

  private async handleJson<T>(response: Response): Promise<T> {
    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }
    return (await response.json()) as T;
  }
}

export const apiClient = new ApiClient({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
});
