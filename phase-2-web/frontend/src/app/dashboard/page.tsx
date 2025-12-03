"use client";

import { useRef } from "react";
import { ExpandableInput } from "@/components/expandable-input";
import { TaskList, TaskListRef } from "@/components/task-list";

export default function DashboardPage() {
  const taskListRef = useRef<TaskListRef>(null);

  const handleTaskCreated = () => {
    taskListRef.current?.refresh();
  };

  return (
    <div>
      <ExpandableInput onTaskCreated={handleTaskCreated} />
      <TaskList ref={taskListRef} />
    </div>
  );
}
