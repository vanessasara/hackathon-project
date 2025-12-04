"use client";

import { useRef, useState, useEffect, use } from "react";
import { motion } from "framer-motion";
import { Tag } from "lucide-react";
import { TaskList, TaskListRef } from "@/components/task-list";
import { ExpandableInput } from "@/components/expandable-input";
import { labelsApi } from "@/lib/api";
import { getToken, useSession } from "@/lib/auth-client";
import { Label } from "@/types";

interface LabelPageProps {
  params: Promise<{ labelId: string }>;
}

export default function LabelPage({ params }: LabelPageProps) {
  const { labelId } = use(params);
  const { data: session } = useSession();
  const taskListRef = useRef<TaskListRef>(null);
  const [label, setLabel] = useState<Label | null>(null);
  const [loading, setLoading] = useState(true);

  const labelIdNum = parseInt(labelId, 10);

  useEffect(() => {
    const fetchLabel = async () => {
      const { data: tokenData, error: tokenError } = await getToken();
      if (tokenError || !tokenData?.token) {
        setLoading(false);
        return;
      }

      try {
        const data = await labelsApi.get(tokenData.token, labelIdNum);
        setLabel(data);
      } catch (err) {
        console.error("Failed to fetch label:", err);
      } finally {
        setLoading(false);
      }
    };

    if (session?.user && !isNaN(labelIdNum)) {
      fetchLabel();
    }
  }, [session, labelIdNum]);

  const handleTaskCreated = () => {
    taskListRef.current?.refresh();
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto"
        />
        <p className="mt-4 text-muted-foreground">Loading...</p>
      </div>
    );
  }

  if (!label) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Label not found</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Label Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3"
      >
        <Tag className="w-6 h-6 text-muted-foreground" />
        <h1 className="text-xl font-medium">{label.name}</h1>
      </motion.div>

      {/* Input */}
      <ExpandableInput onTaskCreated={handleTaskCreated} />

      {/* Task List */}
      <TaskList
        ref={taskListRef}
        filter="active"
        labelId={labelIdNum}
        emptyMessage={`No notes with label "${label.name}"`}
        emptyDescription="Notes with this label will appear here"
      />
    </div>
  );
}
