"use client";

import { useState, useEffect, useImperativeHandle, forwardRef } from "react";
import { Task } from "@/types";
import { tasksApi } from "@/lib/api";
import { TaskItem } from "./task-item";
import { getToken, useSession } from "@/lib/auth-client";

export interface TaskListRef {
  refresh: () => Promise<void>;
}

export const TaskList = forwardRef<TaskListRef>((props, ref) => {
  const { data: session } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) {
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const data = await tasksApi.list(tokenData.token);
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  // Expose refresh function to parent via ref
  useImperativeHandle(ref, () => ({
    refresh: fetchTasks,
  }));

  // Fetch tasks when session becomes available
  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg shadow-sm">
        <div className="text-4xl mb-4">📝</div>
        <h3 className="text-lg font-medium text-gray-900">No tasks yet</h3>
        <p className="mt-2 text-gray-600">
          Create your first task to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onUpdate={fetchTasks} onDelete={fetchTasks} />
      ))}
    </div>
  );
});

TaskList.displayName = "TaskList";
