import type {
  Task,
  TaskCreate,
  TaskUpdate,
  TaskFilter,
  Label,
  LabelCreate,
  LabelUpdate,
  TaskImage,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";  // Empty string uses same origin + Next.js rewrites

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
  list: (
    token: string,
    filter: TaskFilter = "active",
    labelId?: number
  ) => {
    const params = new URLSearchParams({ filter });
    if (labelId !== undefined) {
      params.append("label_id", labelId.toString());
    }
    return apiClient<Task[]>(`/api/tasks?${params.toString()}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  },

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

  restore: (token: string, id: number) =>
    apiClient<Task>(`/api/tasks/${id}/restore`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    }),

  permanentDelete: (token: string, id: number) =>
    apiClient<void>(`/api/tasks/${id}/permanent`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),

  emptyTrash: (token: string) =>
    apiClient<void>("/api/tasks/trash/empty", {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),

  toggleComplete: (token: string, id: number) =>
    apiClient<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
    }),

  addLabel: (token: string, taskId: number, labelId: number) =>
    apiClient<{ message: string }>(`/api/tasks/${taskId}/labels/${labelId}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    }),

  removeLabel: (token: string, taskId: number, labelId: number) =>
    apiClient<void>(`/api/tasks/${taskId}/labels/${labelId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),
};

// Label API functions
export const labelsApi = {
  list: (token: string) =>
    apiClient<Label[]>("/api/labels", {
      headers: { Authorization: `Bearer ${token}` },
    }),

  create: (token: string, data: LabelCreate) =>
    apiClient<Label>("/api/labels", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),

  get: (token: string, id: number) =>
    apiClient<Label>(`/api/labels/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    }),

  update: (token: string, id: number, data: LabelUpdate) =>
    apiClient<Label>(`/api/labels/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),

  delete: (token: string, id: number) =>
    apiClient<void>(`/api/labels/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),
};

// Image API functions
export const imagesApi = {
  upload: async (token: string, taskId: number, file: File): Promise<TaskImage> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/api/images/tasks/${taskId}/images`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Upload failed: ${response.status}`);
    }

    return response.json();
  },

  list: (token: string, taskId: number) =>
    apiClient<TaskImage[]>(`/api/images/tasks/${taskId}/images`, {
      headers: { Authorization: `Bearer ${token}` },
    }),

  delete: (token: string, imageId: number) =>
    apiClient<void>(`/api/images/${imageId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    }),
};
