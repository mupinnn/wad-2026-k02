import { computed, ref } from "vue";
import { FALLBACK_HTTP, FALLBACK_NETWORK, messageFrom, resolveUrl } from "@/lib/api";

const TOKEN_KEY = "access_token";

function readToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export const token = ref<string | null>(readToken());

function setToken(value: string | null) {
  token.value = value;
  try {
    if (value) localStorage.setItem(TOKEN_KEY, value);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {
    // penyimpanan tidak tersedia: token tetap hidup di memori
  }
}

export function clearToken() {
  setToken(null);
}

type Result<T> = { ok: true; data: T } | { ok: false; message: string };

async function post<T>(path: string, body: unknown): Promise<Result<T>> {
  try {
    const response = await fetch(resolveUrl(path), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      return { ok: false, message: messageFrom(payload) ?? FALLBACK_HTTP };
    }
    return { ok: true, data: (payload as { data: T }).data };
  } catch {
    return { ok: false, message: FALLBACK_NETWORK };
  }
}

export function useAuth() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const isLoggedIn = computed(() => token.value !== null);

  async function login(email: string, password: string) {
    loading.value = true;
    error.value = null;
    const result = await post<{ access_token: string }>("/auth/login", { email, password });
    loading.value = false;
    if (!result.ok) {
      error.value = result.message;
      return false;
    }
    setToken(result.data.access_token);
    return true;
  }

  async function register(nama: string, email: string, password: string) {
    loading.value = true;
    error.value = null;
    const result = await post("/auth/register", { nama, email, password });
    if (!result.ok) {
      loading.value = false;
      error.value = result.message;
      return false;
    }
    return login(email, password);
  }

  return { token, isLoggedIn, loading, error, login, register, logout: clearToken };
}
