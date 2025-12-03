"use client";

import { useState, useEffect, useImperativeHandle, forwardRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Task, TaskFilter, Label } from "@/types";
import { tasksApi, labelsApi } from "@/lib/api";
import { TaskCard } from "./task-card";
import { getToken, useSession } from "@/lib/auth-client";
import { useDashboard } from "@/app/dashboard/dashboard-client";

export interface TaskListRef {
  refresh: () => Promise<void>;
}

export interface TaskListProps {
  filter?: TaskFilter;
  labelId?: number;
  emptyMessage?: string;
  emptyDescription?: string;
  showPinnedSection?: boolean;
}

export const TaskList = forwardRef<TaskListRef, TaskListProps>(
  (
    {
      filter = "active",
      labelId,
      emptyMessage = "Notes you add appear here",
      emptyDescription = 'Click the "Take a note..." field above to create your first note',
      showPinnedSection = true,
    },
    ref
  ) => {
    const { data: session } = useSession();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [labels, setLabels] = useState<Label[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { viewMode } = useDashboard();

    const fetchTasks = async (refetchLabels = false) => {
      const { data: tokenData, error: tokenError } = await getToken();
      if (tokenError || !tokenData?.token) {
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        // Only fetch labels if we don't have them or explicitly asked to refetch
        if (labels.length === 0 || refetchLabels) {
          const [tasksData, labelsData] = await Promise.all([
            tasksApi.list(tokenData.token, filter, labelId),
            labelsApi.list(tokenData.token),
          ]);
          setTasks(tasksData);
          setLabels(labelsData);
        } else {
          // Just fetch tasks - labels are cached
          const tasksData = await tasksApi.list(tokenData.token, filter, labelId);
          setTasks(tasksData);
        }
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

    // Fetch tasks when session becomes available or filter/labelId changes
    useEffect(() => {
      if (session?.user) {
        fetchTasks();
      }
    }, [session, filter, labelId]);

    if (loading) {
      return (
        <div className="text-center py-12">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto"
          />
          <p className="mt-4 text-muted-foreground">Loading notes...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="text-center py-12">
          <p className="text-destructive">{error}</p>
        </div>
      );
    }

    if (tasks.length === 0) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-16"
        >
          <div className="w-24 h-24 mx-auto mb-6 text-muted-foreground opacity-50">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M9 2H15M12 18V22M12 22H8M12 22H16M3 5V11C3 14.3137 5.68629 17 9 17H15C18.3137 17 21 14.3137 21 11V5C21 3.89543 20.1046 3 19 3H5C3.89543 3 3 3.89543 3 5Z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <h3 className="text-xl font-normal text-foreground mb-2">{emptyMessage}</h3>
          <p className="text-muted-foreground">{emptyDescription}</p>
        </motion.div>
      );
    }

    // Separate pinned and unpinned tasks
    const pinnedTasks = showPinnedSection
      ? tasks.filter((t) => t.pinned)
      : [];
    const otherTasks = showPinnedSection
      ? tasks.filter((t) => !t.pinned)
      : tasks;

    const gridClassName = viewMode === "grid" ? "masonry-grid" : "list-view";

    return (
      <div className="space-y-8">
        {/* Pinned section */}
        {pinnedTasks.length > 0 && (
          <section>
            <h2 className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-3 px-2">
              Pinned
            </h2>
            <div className={gridClassName}>
              <AnimatePresence mode="popLayout">
                {pinnedTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    allLabels={labels}
                    onUpdate={fetchTasks}
                    onDelete={fetchTasks}
                  />
                ))}
              </AnimatePresence>
            </div>
          </section>
        )}

        {/* Others section */}
        {otherTasks.length > 0 && (
          <section>
            {pinnedTasks.length > 0 && (
              <h2 className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-3 px-2">
                Others
              </h2>
            )}
            <div className={gridClassName}>
              <AnimatePresence mode="popLayout">
                {otherTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    allLabels={labels}
                    onUpdate={fetchTasks}
                    onDelete={fetchTasks}
                  />
                ))}
              </AnimatePresence>
            </div>
          </section>
        )}
      </div>
    );
  }
);

TaskList.displayName = "TaskList";
