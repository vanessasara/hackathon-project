"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Repeat, X, Calendar } from "lucide-react";

/**
 * Recurring task pattern options
 * Part B: Advanced Features - Recurring Tasks
 */
export type RecurrenceRule = "daily" | "weekly" | "monthly" | "weekdays" | null;

interface RecurringPickerProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (rule: RecurrenceRule, endDate?: Date | null) => void;
  currentRule?: RecurrenceRule;
  currentEndDate?: string | null;
}

const RECURRENCE_OPTIONS: { value: RecurrenceRule; label: string; description: string }[] = [
  { value: "daily", label: "Daily", description: "Repeats every day" },
  { value: "weekly", label: "Weekly", description: "Repeats every week" },
  { value: "monthly", label: "Monthly", description: "Repeats every month" },
  { value: "weekdays", label: "Weekdays", description: "Monday through Friday" },
];

export function RecurringPicker({
  isOpen,
  onClose,
  onSelect,
  currentRule,
  currentEndDate,
}: RecurringPickerProps) {
  const [showEndDatePicker, setShowEndDatePicker] = useState(false);
  const [selectedRule, setSelectedRule] = useState<RecurrenceRule>(currentRule || null);
  const [endDate, setEndDate] = useState(currentEndDate || "");

  const handleRuleSelect = (rule: RecurrenceRule) => {
    setSelectedRule(rule);
    if (rule === null) {
      // Remove recurrence
      onSelect(null, null);
      onClose();
    }
  };

  const handleSave = () => {
    const parsedEndDate = endDate ? new Date(endDate) : null;
    onSelect(selectedRule, parsedEndDate);
    onClose();
  };

  const handleRemoveRecurrence = () => {
    onSelect(null, null);
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
              <Repeat className="w-5 h-5 text-muted-foreground" />
              <h2 className="text-lg font-medium">
                {showEndDatePicker ? "End date" : "Repeat"}
              </h2>
            </div>
            <button
              onClick={() => {
                if (showEndDatePicker) {
                  setShowEndDatePicker(false);
                } else {
                  onClose();
                }
              }}
              className="p-1 rounded-full hover:bg-card-hover transition-colors"
            >
              <X className="w-5 h-5 text-muted-foreground" />
            </button>
          </div>

          {showEndDatePicker ? (
            /* End date picker */
            <div className="p-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-1">
                  Stop repeating after
                </label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  min={new Date().toISOString().split("T")[0]}
                  className="w-full px-3 py-2 bg-input-bg rounded-lg text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
                <p className="mt-1 text-xs text-muted-foreground">
                  Leave empty for no end date
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setEndDate("")}
                  className="flex-1 py-2 bg-card-hover text-foreground rounded-lg font-medium hover:bg-card-hover/80 transition-colors"
                >
                  Clear
                </button>
                <button
                  onClick={handleSave}
                  className="flex-1 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
                >
                  Save
                </button>
              </div>
            </div>
          ) : (
            /* Recurrence options */
            <div className="py-2">
              {RECURRENCE_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleRuleSelect(option.value)}
                  className={`w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center justify-between ${
                    selectedRule === option.value ? "bg-primary/10" : ""
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Repeat className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <span className="text-foreground block">{option.label}</span>
                      <span className="text-xs text-muted-foreground">
                        {option.description}
                      </span>
                    </div>
                  </div>
                  {selectedRule === option.value && (
                    <div className="w-2 h-2 rounded-full bg-primary" />
                  )}
                </button>
              ))}

              {/* End date option */}
              {selectedRule && (
                <button
                  onClick={() => setShowEndDatePicker(true)}
                  className="w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center gap-3 border-t border-border mt-2"
                >
                  <Calendar className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <span className="text-foreground block">Set end date</span>
                    {endDate && (
                      <span className="text-xs text-muted-foreground">
                        Ends {new Date(endDate).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </button>
              )}

              {/* Save button when a rule is selected */}
              {selectedRule && (
                <div className="px-4 pt-3 pb-2">
                  <button
                    onClick={handleSave}
                    className="w-full py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
                  >
                    Save
                  </button>
                </div>
              )}

              {/* Remove recurrence */}
              {currentRule && (
                <>
                  <div className="my-2 mx-4 border-t border-border" />
                  <button
                    onClick={handleRemoveRecurrence}
                    className="w-full px-4 py-3 text-left hover:bg-card-hover transition-colors flex items-center gap-3 text-destructive"
                  >
                    <X className="w-5 h-5" />
                    <span>Remove recurrence</span>
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
