"use client";

import { useRef, useEffect } from "react";
import { ExpandableInput } from "@/components/expandable-input";
import { TaskList, TaskListRef } from "@/components/task-list";

export default function DashboardPage() {
  const taskListRef = useRef<TaskListRef>(null);

  const handleTaskCreated = () => {
    taskListRef.current?.refresh();
  };

  // Listen for tasks created via chat
  useEffect(() => {
    const handleChatTaskCreated = () => {
      taskListRef.current?.refresh();
    };

    window.addEventListener("taskCreated", handleChatTaskCreated);

    return () => {
      window.removeEventListener("taskCreated", handleChatTaskCreated);
    };
  }, []);

  return (
    <div>
      <ExpandableInput onTaskCreated={handleTaskCreated} />
      <TaskList ref={taskListRef} />
    </div>
  );
}
