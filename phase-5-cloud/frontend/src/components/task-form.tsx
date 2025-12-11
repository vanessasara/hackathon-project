"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";
import { Check, Pin, Image, Archive, X, Clock, Repeat } from "lucide-react";
import { tasksApi, imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";
import { ColorPicker } from "@/components/color-picker";
import { ColorKey, getColor } from "@/lib/colors";
import { ReminderPicker } from "@/components/reminder-picker";
import { RecurringPicker, RecurrenceRule } from "@/components/recurring-picker";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

interface TaskFormProps {
  onTaskCreated?: () => void;
}

interface PendingImage {
  file: File;
  preview: string;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [color, setColor] = useState<ColorKey>("default");
  const [pinned, setPinned] = useState(false);
  const [pendingImages, setPendingImages] = useState<PendingImage[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  // Part B: Advanced Features - Reminders and Recurring Tasks
  const [reminderAt, setReminderAt] = useState<Date | null>(null);
  const [showReminderPicker, setShowReminderPicker] = useState(false);
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrenceRule, setRecurrenceRule] = useState<RecurrenceRule>(null);
  const [recurrenceEnd, setRecurrenceEnd] = useState<Date | null>(null);
  const [showRecurringPicker, setShowRecurringPicker] = useState(false);
  const formRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  const backgroundColor = getColor(color, isDark);
  const isColored = color !== "default";

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (formRef.current && !formRef.current.contains(event.target as Node)) {
        handleClose();
      }
    }
    if (isExpanded) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isExpanded, title, description]);

  // Focus title when expanded
  useEffect(() => {
    if (isExpanded && titleRef.current) {
      titleRef.current.focus();
    }
  }, [isExpanded]);

  const handleClose = async () => {
    if (title.trim() || description.trim()) {
      await handleSubmit();
    }
    resetForm();
  };

  const resetForm = () => {
    setIsExpanded(false);
    setTitle("");
    setDescription("");
    setColor("default");
    setPinned(false);
    // Revoke object URLs to avoid memory leaks
    pendingImages.forEach((img) => URL.revokeObjectURL(img.preview));
    setPendingImages([]);
    setError("");
    // Part B: Reset reminder and recurring state
    setReminderAt(null);
    setIsRecurring(false);
    setRecurrenceRule(null);
    setRecurrenceEnd(null);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const newImages: PendingImage[] = [];
    for (const file of Array.from(files)) {
      // Validate type
      if (!ALLOWED_TYPES.includes(file.type)) {
        setError("Invalid file type. Use JPEG, PNG, GIF, or WebP.");
        continue;
      }
      // Validate size
      if (file.size > MAX_FILE_SIZE) {
        setError("File too large. Maximum size is 5MB.");
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

  const handleSubmit = async () => {
    // Allow creating if there's title, description, OR images
    if (!title.trim() && !description.trim() && pendingImages.length === 0) {
      return;
    }

    // Get JWT token
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) {
      setError("You must be logged in");
      return;
    }

    setLoading(true);
    try {
      // Create the task first
      const task = await tasksApi.create(tokenData.token, {
        title: title.trim() || "Untitled",
        description: description.trim() || undefined,
        color,
        pinned,
        // Part B: Advanced Features
        reminder_at: reminderAt?.toISOString(),
        is_recurring: isRecurring,
        recurrence_rule: recurrenceRule || undefined,
        recurrence_end: recurrenceEnd?.toISOString(),
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
      resetForm();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      ref={formRef}
      layout
      className={`
        mx-auto max-w-xl mb-8 rounded-lg shadow-md overflow-hidden
        transition-colors duration-200
        ${isColored ? "border-transparent" : "border border-card-border bg-card"}
      `}
      style={{
        backgroundColor: isColored ? backgroundColor : undefined,
      }}
    >
      {error && (
        <div className="px-4 py-2 text-sm text-destructive bg-destructive/10">
          {error}
        </div>
      )}

      <AnimatePresence mode="wait">
        {!isExpanded ? (
          /* Collapsed state */
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
                className="p-2 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
                aria-label="New list"
              >
                <Check className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        ) : (
          /* Expanded state */
          <motion.div
            key="expanded"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {/* Title row */}
            <div className="flex items-center px-4 pt-3 gap-2">
              <input
                ref={titleRef}
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Title"
                maxLength={200}
                className="flex-1 bg-transparent text-foreground font-medium placeholder:text-muted-foreground focus:outline-none"
              />
              <motion.button
                type="button"
                onClick={() => setPinned(!pinned)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className={`p-2 rounded-full transition-colors ${
                  pinned
                    ? "text-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-black/10"
                }`}
                aria-label={pinned ? "Unpin" : "Pin"}
              >
                <Pin className={`w-5 h-5 ${pinned ? "fill-current" : ""}`} />
              </motion.button>
            </div>

            {/* Description */}
            <div className="px-4 py-2">
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Take a note..."
                maxLength={1000}
                rows={3}
                className="w-full bg-transparent text-foreground placeholder:text-muted-foreground focus:outline-none resize-none"
              />
            </div>

            {/* Pending Images Preview */}
            {pendingImages.length > 0 && (
              <div className="px-4 py-2 flex flex-wrap gap-2">
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

            {/* Reminder/Recurring indicators */}
            {(reminderAt || isRecurring) && (
              <div className="flex items-center gap-2 px-4 pb-2">
                {reminderAt && (
                  <span className="inline-flex items-center gap-1 text-xs text-muted-foreground bg-card-hover px-2 py-1 rounded">
                    <Clock className="w-3 h-3" />
                    {reminderAt.toLocaleString(undefined, {
                      dateStyle: "short",
                      timeStyle: "short",
                    })}
                  </span>
                )}
                {isRecurring && recurrenceRule && (
                  <span className="inline-flex items-center gap-1 text-xs text-muted-foreground bg-card-hover px-2 py-1 rounded">
                    <Repeat className="w-3 h-3" />
                    {recurrenceRule.charAt(0).toUpperCase() + recurrenceRule.slice(1)}
                  </span>
                )}
              </div>
            )}

            {/* Toolbar */}
            <div className="flex items-center justify-between px-2 py-2 border-t border-card-border/30">
              <div className="flex items-center gap-0.5">
                <ColorPicker
                  selectedColor={color}
                  onColorChange={setColor}
                  size="sm"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-2 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
                  aria-label="Add image"
                >
                  <Image className="w-4 h-4" />
                </button>
                {/* Part B: Reminder button */}
                <button
                  type="button"
                  onClick={() => setShowReminderPicker(true)}
                  className={`p-2 rounded-full transition-colors ${
                    reminderAt
                      ? "text-primary"
                      : "text-muted-foreground hover:text-foreground hover:bg-black/10"
                  }`}
                  aria-label="Set reminder"
                >
                  <Clock className="w-4 h-4" />
                </button>
                {/* Part B: Recurring button */}
                <button
                  type="button"
                  onClick={() => setShowRecurringPicker(true)}
                  className={`p-2 rounded-full transition-colors ${
                    isRecurring
                      ? "text-primary"
                      : "text-muted-foreground hover:text-foreground hover:bg-black/10"
                  }`}
                  aria-label="Set recurring"
                >
                  <Repeat className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  className="p-2 rounded-full text-muted-foreground hover:text-foreground hover:bg-black/10 transition-colors"
                  aria-label="Archive"
                >
                  <Archive className="w-4 h-4" />
                </button>
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

      {/* Part B: Reminder Picker Modal */}
      <ReminderPicker
        isOpen={showReminderPicker}
        onClose={() => setShowReminderPicker(false)}
        onSelect={(date) => setReminderAt(date)}
        currentReminder={reminderAt?.toISOString()}
      />

      {/* Part B: Recurring Picker Modal */}
      <RecurringPicker
        isOpen={showRecurringPicker}
        onClose={() => setShowRecurringPicker(false)}
        onSelect={(rule, endDate) => {
          setRecurrenceRule(rule);
          setIsRecurring(!!rule);
          setRecurrenceEnd(endDate || null);
        }}
        currentRule={recurrenceRule}
        currentEndDate={recurrenceEnd?.toISOString()}
      />
    </motion.div>
  );
}
