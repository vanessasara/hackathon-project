import type { Task, TaskCreate, TaskUpdate } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

// Task API functions
export const tasksApi = {
  list: (token: string) =>
    apiClient<Task[]>("/api/tasks", {
      headers: { Authorization: `Bearer ${token}` },
    }),

  create: (token: string, data: TaskCreate) =>
    apiClient<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),

  get: (token: string, id: number) =>
    apiClient<Task>(`/api/tasks/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    }),

  update: (token: string, id: number, data: TaskUpdate) =>
    apiClient<Task>(`/api/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),

  delete: (token: string, id: number) =>
    apiClient<void>(`/api/tasks/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),

  toggleComplete: (token: string, id: number) =>
    apiClient<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
    }),
};
