"use client";

import { useRef } from "react";
import { TaskForm } from "@/components/task-form";
import { TaskList, TaskListRef } from "@/components/task-list";

export default function DashboardPage() {
  const taskListRef = useRef<TaskListRef>(null);

  const handleTaskCreated = () => {
    taskListRef.current?.refresh();
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Tasks</h1>
      <TaskForm onTaskCreated={handleTaskCreated} />
      <TaskList ref={taskListRef} />
    </div>
  );
}
