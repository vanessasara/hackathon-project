"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { Trash2, AlertTriangle } from "lucide-react";
import { TaskList, TaskListRef } from "@/components/task-list";
import { tasksApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

export default function TrashPage() {
  const taskListRef = useRef<TaskListRef>(null);
  const [isEmptying, setIsEmptying] = useState(false);

  const handleEmptyTrash = async () => {
    if (!confirm("Are you sure you want to permanently delete all items in trash?")) {
      return;
    }

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setIsEmptying(true);
    try {
      await tasksApi.emptyTrash(tokenData.token);
      taskListRef.current?.refresh();
    } catch (err) {
      console.error("Failed to empty trash:", err);
    } finally {
      setIsEmptying(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Trash Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <Trash2 className="w-6 h-6 text-muted-foreground" />
          <h1 className="text-xl font-medium">Trash</h1>
        </div>
        <button
          onClick={handleEmptyTrash}
          disabled={isEmptying}
          className="px-4 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 rounded-lg transition-colors disabled:opacity-50"
        >
          {isEmptying ? "Emptying..." : "Empty Trash"}
        </button>
      </motion.div>

      {/* 7-day Warning Banner */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="flex items-center gap-3 px-4 py-3 bg-amber-500/10 border border-amber-500/20 rounded-lg"
      >
        <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0" />
        <p className="text-sm text-amber-700 dark:text-amber-400">
          Notes in Trash are deleted after 7 days
        </p>
      </motion.div>

      {/* Task List */}
      <TaskList
        ref={taskListRef}
        filter="trash"
        showPinnedSection={false}
        emptyMessage="No notes in Trash"
        emptyDescription="Notes you delete will appear here"
      />
    </div>
  );
}
