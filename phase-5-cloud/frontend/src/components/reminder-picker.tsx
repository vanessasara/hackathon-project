"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Clock, Calendar, X } from "lucide-react";

interface ReminderPickerProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (date: Date | null) => void;
  currentReminder?: string | null;
}

export function ReminderPicker({
  isOpen,
  onClose,
  onSelect,
  currentReminder,
}: ReminderPickerProps) {
  const [showCustomPicker, setShowCustomPicker] = useState(false);
  const [customDate, setCustomDate] = useState("");
  const [customTime, setCustomTime] = useState("08:00");

  const now = new Date();
  const today8PM = new Date(now);
  today8PM.setHours(20, 0, 0, 0);

  const tomorrow8AM = new Date(now);
  tomorrow8AM.setDate(tomorrow8AM.getDate() + 1);
  tomorrow8AM.setHours(8, 0, 0, 0);

  const nextMonday8AM = new Date(now);
  const daysUntilMonday = (8 - now.getDay()) % 7 || 7;
  nextMonday8AM.setDate(nextMonday8AM.getDate() + daysUntilMonday);
  nextMonday8AM.setHours(8, 0, 0, 0);

  const presets = [
    {
      label: "Today 8:00 PM",
      date: today8PM,
      enabled: now < today8PM,
    },
    {
      label: "Tomorrow 8:00 AM",
      date: tomorrow8AM,
      enabled: true,
    },
    {
      label: `Next week ${nextMonday8AM.toLocaleDateString("en-US", { weekday: "long" })} 8:00 AM`,
      date: nextMonday8AM,
      enabled: true,
    },
  ];

  const handlePresetSelect = (date: Date) => {
    onSelect(date);
    onClose();
  };

  const handleCustomSelect = () => {
    if (!customDate) return;
    // Parse date and time together as local time (not UTC)
    // Format: "2025-12-09T19:10" is interpreted as local timezone
    const date = new Date(`${customDate}T${customTime}:00`);
    onSelect(date);
    onClose();
    setShowCustomPicker(false);
  };

  const handleRemoveReminder = () => {
    onSelect(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
          className="bg-card rounded-lg shadow-xl w-full max-w-xs overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-border">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-muted-foreground" />
              <h2 className="text-lg font-medium">
                {showCustomPicker ? "Pick date & time" : "Reminder"}
              </h2>
            </div>
            <button
              onClick={() => {
                if (showCustomPicker) {
                  setShowCustomPicker(false);
                } else {
                  onClose();
                }
              }}
              className="p-1 rounded-full hover:bg-card-hover transition-colors"
            >
              <X className="w-5 h-5 text-muted-foreground" />
            </button>
          </div>

          {showCustomPicker ? (
            /* Custom date/time picker */
            <div className="p-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1">
                  Date
                </label>
                <input
                  type="date"
                  value={customDate}
                  onChange={(e) => setCustomDate(e.target.value)}
                  min={new Date().toISOString().split("T")[0]}
                  className="w-full px-3 py-2 bg-input-bg rounded-lg text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1">
                  Time
                </label>
                <input
                  type="time"
                  value={customTime}
                  onChange={(e) => setCustomTime(e.target.value)}
                  className="w-full px-3 py-2 bg-input-bg rounded-lg text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <button
                onClick={handleCustomSelect}
                disabled={!customDate}
                className="w-full py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50"
              >
                Save
              </button>
            </div>
          ) : (
            /* Preset options */
            <div className="py-2">
              {presets.map(
                (preset, index) =>
                  preset.enabled && (
                    <button
                      key={index}
                      onClick={() => handlePresetSelect(preset.date)}
                      className="w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center gap-3"
                    >
                      <Clock className="w-5 h-5 text-muted-foreground" />
                      <span className="text-foreground">{preset.label}</span>
                    </button>
                  )
              )}
              <button
                onClick={() => setShowCustomPicker(true)}
                className="w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center gap-3"
              >
                <Calendar className="w-5 h-5 text-muted-foreground" />
                <span className="text-foreground">Pick date & time</span>
              </button>

              {currentReminder && (
                <>
                  <div className="my-2 mx-4 border-t border-border" />
                  <button
                    onClick={handleRemoveReminder}
                    className="w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center gap-3 text-destructive"
                  >
                    <X className="w-5 h-5" />
                    <span>Remove reminder</span>
                  </button>
                </>
              )}
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
