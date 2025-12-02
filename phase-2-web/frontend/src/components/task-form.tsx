"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { tasksApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

interface TaskFormProps {
  onTaskCreated?: () => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (title.length > 200) {
      setError("Title must be 200 characters or less");
      return;
    }
    if (description && description.length > 1000) {
      setError("Description must be 1000 characters or less");
      return;
    }

    // Get JWT token
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) {
      setError("You must be logged in");
      return;
    }

    setLoading(true);
    try {
      await tasksApi.create(tokenData.token, {
        title: title.trim(),
        description: description.trim() || undefined,
      });
      setTitle("");
      setDescription("");
      onTaskCreated?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-4 mb-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
            {error}
          </div>
        )}
        <Input
          label="Task Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          maxLength={200}
          disabled={loading}
        />
        <div>
          <label
            htmlFor="task-description"
            className="mb-1.5 block text-sm font-medium text-gray-700"
          >
            Description (optional)
          </label>
          <textarea
            id="task-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details..."
            maxLength={1000}
            rows={3}
            disabled={loading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500 text-sm"
          />
          <p className="mt-1 text-xs text-gray-500">
            {description.length}/1000 characters
          </p>
        </div>
        <Button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add Task"}
        </Button>
      </form>
    </Card>
  );
}
