"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckSquare, Image, Pin, Bell, Clock, X } from "lucide-react";
import { ColorPicker } from "./color-picker";
import { ReminderPicker } from "./reminder-picker";
import { ColorKey, getColor } from "@/lib/colors";
import { toLocalISOString, formatReminderDate } from "@/lib/date-utils";
import { useTheme } from "next-themes";
import { tasksApi, imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

interface PendingImage {
  file: File;
  preview: string;
}

interface ExpandableInputProps {
  onTaskCreated?: () => void;
}

export function ExpandableInput({ onTaskCreated }: ExpandableInputProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [color, setColor] = useState<ColorKey>("default");
  const [pinned, setPinned] = useState(false);
  const [reminder, setReminder] = useState<Date | null>(null);
  const [showReminderPicker, setShowReminderPicker] = useState(false);
  const [loading, setLoading] = useState(false);
  const [pendingImages, setPendingImages] = useState<PendingImage[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  // Focus title when expanded
  useEffect(() => {
    if (isExpanded && titleRef.current) {
      titleRef.current.focus();
    }
  }, [isExpanded]);

  // Handle click outside to collapse and save
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        handleSave();
      }
    }

    if (isExpanded) {
      document.addEventListener("mousedown", handleClickOutside);
      return () =>
        document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isExpanded, title, content, color, pinned]);

  const handleSave = async () => {
    // Only save if there's content or images
    if (title.trim() || content.trim() || pendingImages.length > 0) {
      const { data: tokenData, error: tokenError } = await getToken();
      if (tokenError || !tokenData?.token) {
        setIsExpanded(false);
        resetForm();
        return;
      }

      setLoading(true);
      try {
        const task = await tasksApi.create(tokenData.token, {
          title: title.trim() || "Untitled",
          description: content.trim() || undefined,
          color,
          pinned,
          reminder_at: reminder ? toLocalISOString(reminder) : undefined,
        });

        // Upload any pending images
        if (pendingImages.length > 0 && task.id) {
          await Promise.all(
            pendingImages.map((img) =>
              imagesApi.upload(tokenData.token, task.id, img.file).catch(() => {
                // Silently fail individual uploads
              })
            )
          );
        }

        onTaskCreated?.();
      } catch {
        // Silently fail - user can retry
      } finally {
        setLoading(false);
      }
    }

    setIsExpanded(false);
    resetForm();
  };

  const resetForm = () => {
    setTitle("");
    setContent("");
    setColor("default");
    setPinned(false);
    setReminder(null);
    // Revoke object URLs to avoid memory leaks
    pendingImages.forEach((img) => URL.revokeObjectURL(img.preview));
    setPendingImages([]);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const newImages: PendingImage[] = [];
    for (const file of Array.from(files)) {
      // Validate type
      if (!ALLOWED_TYPES.includes(file.type)) {
        continue;
      }
      // Validate size
      if (file.size > MAX_FILE_SIZE) {
        continue;
      }
      newImages.push({
        file,
        preview: URL.createObjectURL(file),
      });
    }

    if (newImages.length > 0) {
      setPendingImages((prev) => [...prev, ...newImages].slice(0, 10)); // Max 10
    }

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const removePendingImage = (index: number) => {
    setPendingImages((prev) => {
      const newImages = [...prev];
      URL.revokeObjectURL(newImages[index].preview);
      newImages.splice(index, 1);
      return newImages;
    });
  };

  const handleClose = () => {
    handleSave();
  };

  const backgroundColor = getColor(color, isDark);

  return (
    <div ref={containerRef} className="mb-8 mx-auto max-w-xl">
      <motion.div
        layout
        style={{
          backgroundColor:
            color === "default"
              ? "var(--card)"
              : backgroundColor,
        }}
        className="rounded-lg border border-card-border shadow-sm overflow-hidden"
      >
        <AnimatePresence mode="wait">
          {!isExpanded ? (
            // Collapsed state
            <motion.div
              key="collapsed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsExpanded(true)}
              className="flex items-center justify-between px-4 py-3 cursor-text"
            >
              <span className="text-muted-foreground">Take a note...</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setIsExpanded(true);
                  }}
                  className="p-2 rounded-full hover:bg-card-hover transition-colors"
                >
                  <CheckSquare className="w-5 h-5 text-muted-foreground" />
                </button>
              </div>
            </motion.div>
          ) : (
            // Expanded state
            <motion.div
              key="expanded"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="p-4"
            >
              {/* Title input */}
              <div className="flex items-center gap-2 mb-2">
                <input
                  ref={titleRef}
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Title"
                  maxLength={200}
                  className="flex-1 bg-transparent text-base font-semibold text-foreground placeholder:text-muted-foreground placeholder:font-normal focus:outline-none"
                />
                <motion.button
                  type="button"
                  onClick={() => setPinned(!pinned)}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  className={`p-2 rounded-full transition-colors ${
                    pinned ? "text-foreground" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Pin
                    className={`w-5 h-5 ${pinned ? "fill-current" : ""}`}
                  />
                </motion.button>
              </div>

              {/* Content textarea */}
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Take a note..."
                maxLength={1000}
                rows={3}
                className="w-full bg-transparent text-sm text-muted-foreground placeholder:text-muted-foreground focus:outline-none resize-none"
              />

              {/* Reminder chip */}
              {reminder && (
                <div className="mt-2 flex items-center gap-1">
                  <div className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs bg-primary/10 text-primary">
                    <Clock className="w-3 h-3" />
                    <span>{formatReminderDate(toLocalISOString(reminder))}</span>
                    <button
                      type="button"
                      onClick={() => setReminder(null)}
                      className="ml-1 hover:text-primary/70"
                    >
                      ×
                    </button>
                  </div>
                </div>
              )}

              {/* Pending Images Preview */}
              {pendingImages.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {pendingImages.map((img, index) => (
                    <div key={img.preview} className="relative group">
                      <img
                        src={img.preview}
                        alt={`Pending ${index + 1}`}
                        className="w-16 h-16 object-cover rounded"
                      />
                      <button
                        type="button"
                        onClick={() => removePendingImage(index)}
                        className="absolute -top-1 -right-1 p-0.5 rounded-full bg-destructive text-destructive-foreground opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Hidden file input */}
              <input
                ref={fileInputRef}
                type="file"
                accept={ALLOWED_TYPES.join(",")}
                multiple
                onChange={handleImageSelect}
                className="hidden"
              />

              {/* Toolbar */}
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-card-border">
                <div className="flex items-center gap-1">
                  <motion.button
                    type="button"
                    onClick={() => setShowReminderPicker(true)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className={`p-2 rounded-full transition-colors ${
                      reminder ? "text-foreground" : "text-muted-foreground hover:text-foreground"
                    }`}
                    aria-label="Add reminder"
                  >
                    <Bell className={`w-4 h-4 ${reminder ? "fill-current" : ""}`} />
                  </motion.button>
                  <ColorPicker
                    selectedColor={color}
                    onColorChange={setColor}
                    size="sm"
                  />
                  <motion.button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="p-2 rounded-full text-muted-foreground hover:text-foreground transition-colors"
                    aria-label="Add image"
                  >
                    <Image className="w-4 h-4" />
                  </motion.button>
                </div>
                <motion.button
                  type="button"
                  onClick={handleClose}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={loading}
                  className="px-4 py-1.5 text-sm font-medium text-foreground hover:bg-card-hover rounded transition-colors disabled:opacity-50"
                >
                  {loading ? "Saving..." : "Close"}
                </motion.button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Reminder Picker */}
      <ReminderPicker
        isOpen={showReminderPicker}
        onClose={() => setShowReminderPicker(false)}
        onSelect={(date) => setReminder(date)}
        currentReminder={reminder ? toLocalISOString(reminder) : undefined}
      />
    </div>
  );
}
