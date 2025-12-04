"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import { Archive } from "lucide-react";
import { TaskList, TaskListRef } from "@/components/task-list";

export default function ArchivePage() {
  const taskListRef = useRef<TaskListRef>(null);

  return (
    <div className="space-y-6">
      {/* Archive Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3"
      >
        <Archive className="w-6 h-6 text-muted-foreground" />
        <h1 className="text-xl font-medium">Archive</h1>
      </motion.div>

      {/* Task List */}
      <TaskList
        ref={taskListRef}
        filter="archive"
        showPinnedSection={false}
        emptyMessage="No archived notes"
        emptyDescription="Your archived notes appear here"
      />
    </div>
  );
}
