import { onScopeDispose, ref, toValue, type Ref } from "vue";
import type { UseFetchOptions, UseFetchReturn } from "@/interface/useFetchInterface";
import { FALLBACK_HTTP, FALLBACK_NETWORK, messageFrom, resolveUrl } from "@/lib/api";
import { clearToken, token } from "@/composables/useAuth";

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
    const hasBody = method === "POST" || method === "PATCH";
    const headers = new Headers(options.config?.headers);
    if (hasBody) headers.set("Content-Type", "application/json");
    if (token.value) headers.set("Authorization", `Bearer ${token.value}`);

    try {
      const response = await fetch(resolveUrl(toValue(options.url)), {
        ...options.config,
        method,
        headers,
        body: hasBody ? JSON.stringify(toValue(options.body)) : undefined,
        signal: controller.signal,
      });

      if (id !== requestId) return;

      if (!response.ok) {
        if (response.status === 401) clearToken();
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
