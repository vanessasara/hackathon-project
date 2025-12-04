"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import { toast } from "sonner";
import {
  Pin,
  Bell,
  Archive,
  ArchiveRestore,
  Trash2,
  RotateCcw,
  Clock,
} from "lucide-react";
import { Task, Label, TaskImage } from "@/types";
import { ColorKey, getColor } from "@/lib/colors";
import { toLocalISOString, formatReminderDate } from "@/lib/date-utils";
import { ColorPicker } from "./color-picker";
import { TodoModal } from "./todo-modal";
import { ReminderPicker } from "./reminder-picker";
import { LabelPicker } from "./label-picker";
import { ImageUpload } from "./image-upload";
import { ImageGallery } from "./image-gallery";
import { tasksApi, imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

interface TaskCardProps {
  task: Task;
  allLabels?: Label[];
  onUpdate?: () => void;
  onDelete?: () => void;
}

export function TaskCard({ task, allLabels = [], onUpdate, onDelete }: TaskCardProps) {
  const pathname = usePathname();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showReminderPicker, setShowReminderPicker] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [images, setImages] = useState<TaskImage[]>([]);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  // Fetch images for this task
  useEffect(() => {
    async function fetchImages() {
      const { data: tokenData, error: tokenError } = await getToken();
      if (tokenError || !tokenData?.token) return;

      try {
        const taskImages = await imagesApi.list(tokenData.token, task.id);
        setImages(taskImages);
      } catch {
        // Silently fail
      }
    }
    fetchImages();
  }, [task.id]);

  const handleImageUpload = (image: TaskImage) => {
    setImages((prev) => [...prev, image]);
  };

  const handleImageDelete = (imageId: number) => {
    setImages((prev) => prev.filter((img) => img.id !== imageId));
  };

  const color = (task.color || "default") as ColorKey;
  const backgroundColor = getColor(color, isDark);
  const isPinned = task.pinned || false;
  const isArchived = task.archived || false;
  const isTrashed = task.deleted_at !== null;

  // Get assigned label names
  const assignedLabels = allLabels.filter((label) =>
    task.labels?.includes(label.id)
  );

  // Determine context
  const isTrashView = pathname === "/dashboard/trash";
  const isArchiveView = pathname === "/dashboard/archive";

  const handleToggleComplete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.toggleComplete(tokenData.token, task.id);
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.delete(tokenData.token, task.id);
      onDelete?.();

      // Show toast with undo option
      toast("Note moved to Trash", {
        action: {
          label: "Undo",
          onClick: async () => {
            const { data: undoToken } = await getToken();
            if (undoToken?.token) {
              try {
                await tasksApi.restore(undoToken.token, task.id);
                onUpdate?.();
              } catch {
                // Silently fail
              }
            }
          },
        },
        duration: 5000,
      });
    } catch {
      // Silently fail
    }
  };

  const handlePermanentDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Delete this note forever?")) return;

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.permanentDelete(tokenData.token, task.id);
      onDelete?.();
    } catch {
      // Silently fail
    }
  };

  const handleRestore = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.restore(tokenData.token, task.id);
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handleArchive = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, { archived: true });
      onUpdate?.();

      // Show toast with undo option
      toast("Note archived", {
        action: {
          label: "Undo",
          onClick: async () => {
            const { data: undoToken } = await getToken();
            if (undoToken?.token) {
              try {
                await tasksApi.update(undoToken.token, task.id, { archived: false });
                onUpdate?.();
              } catch {
                // Silently fail
              }
            }
          },
        },
        duration: 5000,
      });
    } catch {
      // Silently fail
    }
  };

  const handleUnarchive = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, { archived: false });
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handlePinToggle = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, { pinned: !isPinned });
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handleColorChange = async (newColor: ColorKey) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, { color: newColor });
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handleReminderChange = async (date: Date | null) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, {
        reminder_at: date ? toLocalISOString(date) : null,
      });
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  const handleModalSave = async (title: string, description: string) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await tasksApi.update(tokenData.token, task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });
      onUpdate?.();
    } catch {
      // Silently fail
    }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 24 }}
        onHoverStart={() => setIsHovered(true)}
        onHoverEnd={() => setIsHovered(false)}
        onClick={() => !isTrashed && setIsModalOpen(true)}
        className={`masonry-item ${isTrashed ? "cursor-default" : "cursor-pointer"} group`}
      >
        <div
          style={{
            backgroundColor:
              color === "default" ? "var(--card)" : backgroundColor,
          }}
          className="rounded-lg border border-card-border hover:shadow-lg transition-shadow overflow-hidden"
        >
          {/* Card content */}
          <div className="p-3">
            {/* Checkbox and title */}
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => {}}
                onClick={handleToggleComplete}
                disabled={isTrashed}
                className="mt-1 h-[18px] w-[18px] rounded-full border-2 border-muted-foreground cursor-pointer checked:bg-muted-foreground checked:border-muted-foreground disabled:opacity-50"
              />
              <div className="flex-1 min-w-0">
                <h3
                  className={`text-base font-semibold text-foreground ${
                    task.completed ? "line-through opacity-50" : ""
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p
                    className={`mt-1 text-sm text-muted-foreground line-clamp-6 ${
                      task.completed ? "line-through opacity-50" : ""
                    }`}
                  >
                    {task.description}
                  </p>
                )}
              </div>
            </div>

            {/* Reminder chip */}
            {task.reminder_at && (
              <div className="mt-2 flex items-center gap-1">
                <div
                  className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs ${
                    new Date(task.reminder_at) < new Date()
                      ? "bg-muted text-muted-foreground"
                      : "bg-primary/10 text-primary"
                  }`}
                >
                  <Clock className="w-3 h-3" />
                  <span>{formatReminderDate(task.reminder_at)}</span>
                </div>
              </div>
            )}

            {/* Label chips */}
            {assignedLabels.length > 0 && (
              <div className="mt-2 flex flex-wrap items-center gap-1">
                {assignedLabels.map((label) => (
                  <span
                    key={label.id}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-muted/50 text-muted-foreground border border-muted"
                  >
                    {label.name}
                  </span>
                ))}
              </div>
            )}

            {/* Image gallery */}
            {images.length > 0 && (
              <div onClick={(e) => e.stopPropagation()}>
                <ImageGallery
                  images={images}
                  onDelete={handleImageDelete}
                  editable={!isTrashed}
                />
              </div>
            )}
          </div>

          {/* Hover toolbar */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: isHovered ? 1 : 0 }}
            className="px-2 pb-2 flex items-center justify-between"
          >
            {isTrashView ? (
              /* Trash view actions */
              <div className="flex items-center gap-1">
                <IconButton
                  icon={RotateCcw}
                  label="Restore"
                  onClick={handleRestore}
                />
                <IconButton
                  icon={Trash2}
                  label="Delete forever"
                  onClick={handlePermanentDelete}
                />
              </div>
            ) : isArchiveView ? (
              /* Archive view actions */
              <div className="flex items-center gap-1">
                <IconButton
                  icon={ArchiveRestore}
                  label="Unarchive"
                  onClick={handleUnarchive}
                />
                <IconButton
                  icon={Trash2}
                  label="Delete"
                  onClick={handleDelete}
                />
              </div>
            ) : (
              /* Normal view actions */
              <>
                <div className="flex items-center gap-1">
                  <IconButton
                    icon={Bell}
                    label="Remind me"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowReminderPicker(true);
                    }}
                    active={!!task.reminder_at}
                  />
                  <div onClick={(e) => e.stopPropagation()}>
                    <LabelPicker
                      taskId={task.id}
                      taskLabels={task.labels || []}
                      onUpdate={onUpdate}
                    />
                  </div>
                  <div onClick={(e) => e.stopPropagation()}>
                    <ColorPicker
                      selectedColor={color}
                      onColorChange={handleColorChange}
                      size="sm"
                    />
                  </div>
                  <div onClick={(e) => e.stopPropagation()}>
                    <ImageUpload
                      taskId={task.id}
                      onUpload={handleImageUpload}
                      size="sm"
                    />
                  </div>
                  <IconButton
                    icon={Archive}
                    label="Archive"
                    onClick={handleArchive}
                  />
                  <IconButton
                    icon={Trash2}
                    label="Delete"
                    onClick={handleDelete}
                  />
                </div>
                <IconButton
                  icon={Pin}
                  label={isPinned ? "Unpin" : "Pin"}
                  onClick={handlePinToggle}
                  active={isPinned}
                />
              </>
            )}
          </motion.div>
        </div>
      </motion.div>

      {/* Edit Modal */}
      {!isTrashed && (
        <TodoModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          task={task}
          onSave={handleModalSave}
          onColorChange={handleColorChange}
          onPinChange={handlePinToggle}
        />
      )}

      {/* Reminder Picker */}
      <ReminderPicker
        isOpen={showReminderPicker}
        onClose={() => setShowReminderPicker(false)}
        onSelect={handleReminderChange}
        currentReminder={task.reminder_at}
      />
    </>
  );
}

// Small icon button component
function IconButton({
  icon: Icon,
  label,
  onClick,
  active = false,
}: {
  icon: React.ElementType;
  label: string;
  onClick: (e: React.MouseEvent) => void;
  active?: boolean;
}) {
  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`p-2 rounded-full hover:bg-card-hover transition-colors ${
        active ? "text-foreground" : "text-muted-foreground"
      }`}
      aria-label={label}
    >
      <Icon className={`w-4 h-4 ${active ? "fill-current" : ""}`} />
    </motion.button>
  );
}
