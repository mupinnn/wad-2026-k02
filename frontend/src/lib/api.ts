export const FALLBACK_HTTP = "Permintaan gagal.";
export const FALLBACK_NETWORK = "Tidak bisa menghubungi server.";

export function resolveUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE || "http://localhost:8000";
  const normalizedBase = base.endsWith("/") ? base : `${base}/`;
  return new URL(path.replace(/^\//, ""), normalizedBase).toString();
}

export function messageFrom(payload: unknown) {
  if (!payload || typeof payload !== "object") return null;

  const record = payload as { message?: unknown; detail?: unknown };
  if (typeof record.message === "string" && record.message) return record.message;
  if (typeof record.detail === "string" && record.detail) return record.detail;
  if (Array.isArray(record.detail)) {
    const msg = (record.detail[0] as { msg?: unknown } | undefined)?.msg;
    if (typeof msg === "string") return msg.replace(/^Value error, /, "");
  }
  if (record.detail != null) return JSON.stringify(record.detail);
  return null;
}
