"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import {
  Pin,
  Bell,
  UserPlus,
  ImagePlus,
  Trash2,
  Archive,
  MoreVertical,
} from "lucide-react";
import { Task } from "@/types";
import { tasksApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";
import { ColorPicker } from "@/components/color-picker";
import { TodoModal } from "@/components/todo-modal";
import { getColor, ColorKey } from "@/lib/colors";

interface TaskItemProps {
  task: Task;
  onUpdate?: () => void;
  onDelete?: () => void;
}

export function TaskItem({ task: initialTask, onUpdate, onDelete }: TaskItemProps) {
  const [task, setTask] = useState(initialTask);
  const [isHovered, setIsHovered] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  const colorKey = (task.color || "default") as ColorKey;
  const backgroundColor = getColor(colorKey, isDark);
  const isColored = colorKey !== "default";

  const handleToggleComplete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    const previousCompleted = task.completed;
    setTask({ ...task, completed: !task.completed });

    try {
      await tasksApi.toggleComplete(tokenData.token, task.id);
      onUpdate?.();
    } catch {
      setTask({ ...task, completed: previousCompleted });
    }
  };

  const handleTogglePin = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    const previousPinned = task.pinned;
    setTask({ ...task, pinned: !task.pinned });

    try {
      await tasksApi.update(tokenData.token, task.id, { pinned: !previousPinned });
      onUpdate?.();
    } catch {
      setTask({ ...task, pinned: previousPinned });
    }
  };

  const handleColorChange = async (color: ColorKey) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    const previousColor = task.color;
    setTask({ ...task, color });

    try {
      await tasksApi.update(tokenData.token, task.id, { color });
      onUpdate?.();
    } catch {
      setTask({ ...task, color: previousColor });
    }
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    try {
      await tasksApi.delete(tokenData.token, task.id);
      onDelete?.();
    } catch {
      console.error("Failed to delete task");
    } finally {
      setLoading(false);
    }
  };

  const handleModalSave = async (title: string, description: string) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      const updated = await tasksApi.update(tokenData.token, task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });
      setTask(updated);
      onUpdate?.();
    } catch (err) {
      console.error("Failed to update task:", err);
    }
  };

  return (
    <>
      <motion.div
        layout
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        whileHover={{ boxShadow: "0 4px 12px rgba(0,0,0,0.15)" }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={() => setIsModalOpen(true)}
        className={`
          relative rounded-lg border cursor-pointer
          transition-colors duration-200
          ${isColored
            ? "border-transparent"
            : "border-card-border bg-card hover:bg-card-hover"
          }
        `}
        style={{
          backgroundColor: isColored ? backgroundColor : undefined,
        }}
      >
        {/* Pin button - top right */}
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: isHovered || task.pinned ? 1 : 0 }}
          onClick={handleTogglePin}
          className={`
            absolute top-2 right-2 p-1.5 rounded-full z-10
            transition-colors
            ${task.pinned
              ? "text-foreground"
              : "text-muted-foreground hover:text-foreground hover:bg-black/10"
            }
          `}
          aria-label={task.pinned ? "Unpin note" : "Pin note"}
        >
          <Pin className={`w-4 h-4 ${task.pinned ? "fill-current" : ""}`} />
        </motion.button>

        {/* Content */}
        <div className="p-3 pr-10">
          {task.title && (
            <h3 className={`
              font-medium text-foreground mb-1
              ${task.completed ? "line-through opacity-60" : ""}
            `}>
              {task.title}
            </h3>
          )}
          {task.description && (
            <p className={`
              text-sm text-muted-foreground line-clamp-4
              ${task.completed ? "line-through opacity-60" : ""}
            `}>
              {task.description}
            </p>
          )}
        </div>

        {/* Toolbar - bottom */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: isHovered ? 1 : 0 }}
          className="flex items-center gap-1 px-3 py-2 mt-1"
        >
          {/* Reminder */}
          <button
            onClick={(e) => e.stopPropagation()}
            className="p-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
            aria-label="Add reminder"
          >
            <Bell className="w-4 h-4" />
          </button>

          {/* Collaborator */}
          <button
            onClick={(e) => e.stopPropagation()}
            className="p-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
            aria-label="Add collaborator"
          >
            <UserPlus className="w-4 h-4" />
          </button>

          {/* Color picker */}
          <div onClick={(e) => e.stopPropagation()}>
            <ColorPicker
              selectedColor={colorKey}
              onColorChange={handleColorChange}
              size="sm"
            />
          </div>

          {/* Add image */}
          <button
            onClick={(e) => e.stopPropagation()}
            className="p-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
            aria-label="Add image"
          >
            <ImagePlus className="w-4 h-4" />
          </button>

          {/* Archive */}
          <button
            onClick={(e) => e.stopPropagation()}
            className="p-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
            aria-label="Archive"
          >
            <Archive className="w-4 h-4" />
          </button>

          {/* More options / Delete */}
          <button
            onClick={handleDelete}
            disabled={loading}
            className="p-1.5 rounded-full text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors disabled:opacity-50"
            aria-label="Delete"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </motion.div>
      </motion.div>

      {/* Edit Modal */}
      <TodoModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        task={task}
        onSave={handleModalSave}
        onColorChange={handleColorChange}
        onPinChange={handleTogglePin}
      />
    </>
  );
}
