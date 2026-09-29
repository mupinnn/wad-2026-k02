import { onScopeDispose, ref, toValue, type MaybeRefOrGetter, type Ref } from "vue";

type HttpMethod = "GET" | "POST" | "DELETE";

interface UseFetchOptions {
  url: MaybeRefOrGetter<string>;
  method?: HttpMethod;
  body?: MaybeRefOrGetter<unknown>;
  immediate?: boolean;
  config?: RequestInit;
}

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  execute: () => Promise<void>;
}

const FALLBACK_HTTP = "Permintaan gagal.";
const FALLBACK_NETWORK = "Tidak bisa menghubungi server.";

function resolveUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE || "http://localhost:8000";
  const normalizedBase = base.endsWith("/") ? base : `${base}/`;
  return new URL(path.replace(/^\//, ""), normalizedBase).toString();
}

// mapping between the error return from FastAPI's validation or our custom structure in `services.py`
function messageFrom(payload: unknown) {
  if (!payload || typeof payload !== "object") return null;

  const record = payload as { detail?: unknown; message?: unknown };
  if (typeof record.detail === "string" && record.detail) return record.detail;
  if (record.detail != null) return JSON.stringify(record.detail);
  if (typeof record.message === "string" && record.message) return record.message;
  return null;
}

function isAbort(cause: unknown) {
  return cause instanceof Error && cause.name === "AbortError";
}

export function useFetch<T>(options: UseFetchOptions): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const loading = ref(false);
  const error = ref<string | null>(null);
  let active: AbortController | null = null;
  let requestId = 0;

  async function execute() {
    active?.abort();
    const controller = new AbortController();
    active = controller;
    const id = ++requestId;

    loading.value = true;
    error.value = null;

    const method = options.method ?? "GET";
    const headers = new Headers(options.config?.headers);
    if (method === "POST") headers.set("Content-Type", "application/json");

    try {
      const response = await fetch(resolveUrl(toValue(options.url)), {
        ...options.config,
        method,
        headers,
        body: method === "POST" ? JSON.stringify(toValue(options.body)) : undefined,
        signal: controller.signal,
      });

      if (id !== requestId) return;

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        error.value = messageFrom(payload) ?? FALLBACK_HTTP;
        data.value = null;
        return;
      }

      data.value = (await response.json()) as T;
    } catch (cause) {
      if (id !== requestId || isAbort(cause)) return;
      error.value = FALLBACK_NETWORK;
      data.value = null;
    } finally {
      if (id === requestId) loading.value = false;
    }
  }

  onScopeDispose(() => active?.abort());

  if (options.immediate !== false) void execute();

  return { data, loading, error, execute };
}
