"use client";

import { useState } from "react";
import { Task } from "@/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { tasksApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

interface TaskItemProps {
  task: Task;
  onUpdate?: () => void;
  onDelete?: () => void;
}

export function TaskItem({ task: initialTask, onUpdate, onDelete }: TaskItemProps) {
  const [task, setTask] = useState(initialTask);
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleToggleComplete = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    // Optimistic update
    const previousCompleted = task.completed;
    setTask({ ...task, completed: !task.completed });

    try {
      await tasksApi.toggleComplete(tokenData.token, task.id);
    } catch (err) {
      // Revert on error
      setTask({ ...task, completed: previousCompleted });
      setError("Failed to update");
    }
  };

  const handleDelete = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    try {
      await tasksApi.delete(tokenData.token, task.id);
      onDelete?.();
    } catch (err) {
      setError("Failed to delete");
      setShowDeleteConfirm(false);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    setError("");
    try {
      const updated = await tasksApi.update(tokenData.token, task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });
      setTask(updated);
      setIsEditing(false);
      onUpdate?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || "");
    setError("");
    setIsEditing(false);
  };

  // Delete confirmation dialog
  if (showDeleteConfirm) {
    return (
      <Card className="p-4 border-red-200 bg-red-50">
        <div className="space-y-3">
          <p className="font-medium text-red-800">Delete this task?</p>
          <p className="text-sm text-red-600">"{task.title}"</p>
          <div className="flex gap-2">
            <Button onClick={handleDelete} variant="danger" size="sm" disabled={loading}>
              {loading ? "Deleting..." : "Delete"}
            </Button>
            <Button onClick={() => setShowDeleteConfirm(false)} variant="secondary" size="sm">
              Cancel
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  // Edit mode
  if (isEditing) {
    return (
      <Card className="p-4">
        <div className="space-y-3">
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
          <div className="flex gap-2">
            <Button onClick={handleSave} disabled={loading} size="sm">
              {loading ? "Saving..." : "Save"}
            </Button>
            <Button onClick={handleCancel} variant="secondary" size="sm">
              Cancel
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  // Normal display
  return (
    <Card className="p-4">
      {error && <p className="text-sm text-red-600 mb-2">{error}</p>}
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 cursor-pointer"
        />
        <div className="flex-1 min-w-0">
          <h3 className={`font-medium ${task.completed ? "line-through text-gray-400" : "text-gray-900"}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? "text-gray-400" : "text-gray-600"}`}>
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => setIsEditing(true)} variant="secondary" size="sm">
            Edit
          </Button>
          <Button onClick={() => setShowDeleteConfirm(true)} variant="danger" size="sm">
            Delete
          </Button>
        </div>
      </div>
    </Card>
  );
}
