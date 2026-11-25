const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
export async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API}${path}`, { ...options, headers: { ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }), ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers ?? {}) } });
  if (!response.ok) throw new Error((await response.json()).detail ?? "Request failed");
  if (response.status === 204) return undefined as T;
  return response.json();
}
export { API };

