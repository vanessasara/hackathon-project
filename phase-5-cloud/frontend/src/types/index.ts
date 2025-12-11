export interface TaskImage {
  id: number;
  task_id: number;
  filename: string;
  url: string;
  size_bytes: number;
  mime_type: string;
  width: number | null;
  height: number | null;
  created_at: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  color: string;
  pinned: boolean;
  archived: boolean;
  deleted_at: string | null;
  reminder_at: string | null;
  created_at: string;
  updated_at: string;
  labels: number[];
  images?: TaskImage[];
}

export interface TaskCreate {
  title: string;
  description?: string;
  color?: string;
  pinned?: boolean;
  reminder_at?: string;
  // Part B: Advanced Features
  is_recurring?: boolean;
  recurrence_rule?: string;
  recurrence_end?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  color?: string;
  pinned?: boolean;
  completed?: boolean;
  archived?: boolean;
  reminder_at?: string | null;
}

export interface Label {
  id: number;
  user_id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface LabelCreate {
  name: string;
}

export interface LabelUpdate {
  name?: string;
}

export interface User {
  id: string;
  email: string;
  name: string | null;
  createdAt: string;
  updatedAt: string;
}

export type TaskFilter = "active" | "trash" | "archive" | "reminders";
