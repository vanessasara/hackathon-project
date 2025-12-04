"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";
import { Pin } from "lucide-react";
import { Task, TaskImage } from "@/types";
import { ColorKey, getColor } from "@/lib/colors";
import { ColorPicker } from "./color-picker";
import { ImageUpload } from "./image-upload";
import { ImageGallery } from "./image-gallery";
import { imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

interface TodoModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: Task;
  onSave: (title: string, description: string) => void;
  onColorChange: (color: ColorKey) => void;
  onPinChange: (e: React.MouseEvent) => void;
}

export function TodoModal({
  isOpen,
  onClose,
  task,
  onSave,
  onColorChange,
  onPinChange,
}: TodoModalProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [loading, setLoading] = useState(false);
  const [images, setImages] = useState<TaskImage[]>([]);
  const titleRef = useRef<HTMLInputElement>(null);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  const colorKey = (task.color || "default") as ColorKey;

  // Reset form when task changes
  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description || "");
  }, [task]);

  // Fetch images when modal opens
  useEffect(() => {
    if (isOpen) {
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
    }
  }, [isOpen, task.id]);

  const handleImageUpload = (image: TaskImage) => {
    setImages((prev) => [...prev, image]);
  };

  const handleImageDelete = (imageId: number) => {
    setImages((prev) => prev.filter((img) => img.id !== imageId));
  };

  // Focus title when modal opens
  useEffect(() => {
    if (isOpen && titleRef.current) {
      setTimeout(() => titleRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") {
        handleSave();
      }
    }
    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      return () => document.removeEventListener("keydown", handleEscape);
    }
  }, [isOpen, title, description]);

  const handleSave = async () => {
    if (!title.trim()) {
      onClose();
      return;
    }

    // Only save if something changed
    if (
      title.trim() !== task.title ||
      description.trim() !== (task.description || "")
    ) {
      setLoading(true);
      try {
        await onSave(title.trim(), description.trim());
      } finally {
        setLoading(false);
      }
    }
    onClose();
  };

  const backgroundColor = getColor(colorKey, isDark);
  const formattedDate = new Date(task.updated_at || task.created_at).toLocaleDateString(
    "en-US",
    {
      month: "short",
      day: "numeric",
      year: "numeric",
    }
  );

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleSave}
            className="fixed inset-0 bg-black/50 z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            style={{
              backgroundColor:
                colorKey === "default" ? "var(--card)" : backgroundColor,
            }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-xl rounded-lg shadow-xl overflow-hidden"
          >
            {/* Title input */}
            <div className="p-4 pb-0">
              <div className="flex items-start gap-2">
                <input
                  ref={titleRef}
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Title"
                  maxLength={200}
                  className="flex-1 bg-transparent text-lg font-semibold text-foreground placeholder:text-muted-foreground placeholder:font-normal focus:outline-none"
                />
                <motion.button
                  type="button"
                  onClick={onPinChange}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className={`p-2 rounded-full transition-colors ${
                    task.pinned
                      ? "text-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Pin className={`w-5 h-5 ${task.pinned ? "fill-current" : ""}`} />
                </motion.button>
              </div>
            </div>

            {/* Content textarea */}
            <div className="px-4 py-2">
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Take a note..."
                maxLength={1000}
                rows={6}
                className="w-full bg-transparent text-sm text-muted-foreground placeholder:text-muted-foreground focus:outline-none resize-none"
              />
            </div>

            {/* Image gallery */}
            {images.length > 0 && (
              <div className="px-4 py-2">
                <ImageGallery
                  images={images}
                  onDelete={handleImageDelete}
                  editable={true}
                />
              </div>
            )}

            {/* Timestamp */}
            <div className="px-4 py-2">
              <span className="text-xs text-muted-foreground">
                Edited {formattedDate}
              </span>
            </div>

            {/* Toolbar */}
            <div className="flex items-center justify-between px-2 py-2 border-t border-card-border">
              <div className="flex items-center gap-1">
                <ColorPicker
                  selectedColor={colorKey}
                  onColorChange={onColorChange}
                  size="sm"
                />
                <ImageUpload
                  taskId={task.id}
                  onUpload={handleImageUpload}
                  size="sm"
                />
              </div>
              <motion.button
                type="button"
                onClick={handleSave}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                disabled={loading}
                className="px-4 py-1.5 text-sm font-medium text-foreground hover:bg-card-hover rounded transition-colors disabled:opacity-50"
              >
                {loading ? "Saving..." : "Close"}
              </motion.button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
