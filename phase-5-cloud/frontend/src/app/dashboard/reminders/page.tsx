"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bell } from "lucide-react";
import { Task } from "@/types";
import { tasksApi } from "@/lib/api";
import { TaskCard } from "@/components/task-card";
import { getToken, useSession } from "@/lib/auth-client";
import { useDashboard } from "@/app/dashboard/dashboard-client";

export default function RemindersPage() {
  const { data: session } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { viewMode } = useDashboard();

  const fetchTasks = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) {
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const data = await tasksApi.list(tokenData.token, "reminders");
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (session?.user) {
      fetchTasks();
    }
  }, [session]);

  const now = new Date();
  const sentTasks = tasks.filter((t) => t.reminder_at && new Date(t.reminder_at) < now);
  const upcomingTasks = tasks.filter((t) => t.reminder_at && new Date(t.reminder_at) >= now);

  const gridClassName = viewMode === "grid" ? "masonry-grid" : "list-view";

  if (loading) {
    return (
      <div className="text-center py-12">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto"
        />
        <p className="mt-4 text-muted-foreground">Loading reminders...</p>
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

  return (
    <div className="space-y-6">
      {/* Reminders Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3"
      >
        <Bell className="w-6 h-6 text-muted-foreground" />
        <h1 className="text-xl font-medium">Reminders</h1>
      </motion.div>

      {tasks.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-16"
        >
          <div className="w-24 h-24 mx-auto mb-6 text-muted-foreground opacity-50">
            <Bell className="w-full h-full" strokeWidth={1} />
          </div>
          <h3 className="text-xl font-normal text-foreground mb-2">
            Notes with upcoming reminders appear here
          </h3>
          <p className="text-muted-foreground">
            Add reminders to your notes to see them here
          </p>
        </motion.div>
      ) : (
        <div className="space-y-8">
          {/* Sent Section */}
          {sentTasks.length > 0 && (
            <section>
              <h2 className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-3 px-2">
                Sent
              </h2>
              <div className={gridClassName}>
                <AnimatePresence mode="popLayout">
                  {sentTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onUpdate={fetchTasks}
                      onDelete={fetchTasks}
                    />
                  ))}
                </AnimatePresence>
              </div>
            </section>
          )}

          {/* Upcoming Section */}
          {upcomingTasks.length > 0 && (
            <section>
              <h2 className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-3 px-2">
                Upcoming
              </h2>
              <div className={gridClassName}>
                <AnimatePresence mode="popLayout">
                  {upcomingTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onUpdate={fetchTasks}
                      onDelete={fetchTasks}
                    />
                  ))}
                </AnimatePresence>
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
