"use client";

import { useState, useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Tag, Check, Plus } from "lucide-react";
import { Label } from "@/types";
import { labelsApi, tasksApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";

interface LabelPickerProps {
  taskId: number;
  taskLabels: number[];
  onUpdate?: () => void;
}

export function LabelPicker({ taskId, taskLabels, onUpdate }: LabelPickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [labels, setLabels] = useState<Label[]>([]);
  const [loading, setLoading] = useState(false);
  const [newLabelName, setNewLabelName] = useState("");
  const [showNewLabelInput, setShowNewLabelInput] = useState(false);
  const [dropdownPosition, setDropdownPosition] = useState({ top: 0, left: 0 });
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Fetch labels when picker opens
  useEffect(() => {
    if (isOpen) {
      fetchLabels();
    }
  }, [isOpen]);

  // Focus input when showing new label input
  useEffect(() => {
    if (showNewLabelInput && inputRef.current) {
      inputRef.current.focus();
    }
  }, [showNewLabelInput]);

  // Handle click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      const target = event.target as Node;
      const isOutsideContainer = containerRef.current && !containerRef.current.contains(target);
      const isOutsideDropdown = dropdownRef.current && !dropdownRef.current.contains(target);

      if (isOutsideContainer && isOutsideDropdown) {
        setIsOpen(false);
        setShowNewLabelInput(false);
        setNewLabelName("");
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isOpen]);

  // Calculate dropdown position when opening
  const updateDropdownPosition = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setDropdownPosition({
        top: rect.top - 8, // Position above the button with small gap
        left: rect.left,
      });
    }
  };

  const fetchLabels = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      const data = await labelsApi.list(tokenData.token);
      setLabels(data);
    } catch {
      // Silently fail
    }
  };

  const handleToggleLabel = async (labelId: number) => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    try {
      const isAssigned = taskLabels.includes(labelId);
      if (isAssigned) {
        await tasksApi.removeLabel(tokenData.token, taskId, labelId);
      } else {
        await tasksApi.addLabel(tokenData.token, taskId, labelId);
      }
      onUpdate?.();
    } catch {
      // Silently fail
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLabel = async () => {
    if (!newLabelName.trim()) return;

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    try {
      const newLabel = await labelsApi.create(tokenData.token, { name: newLabelName.trim() });
      setLabels([...labels, newLabel]);
      // Also assign the new label to this task
      await tasksApi.addLabel(tokenData.token, taskId, newLabel.id);
      onUpdate?.();
      setNewLabelName("");
      setShowNewLabelInput(false);
    } catch {
      // Silently fail
    } finally {
      setLoading(false);
    }
  };

  return (
    <div ref={containerRef} className="relative">
      <motion.button
        ref={buttonRef}
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          updateDropdownPosition();
          setIsOpen(!isOpen);
        }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        className="p-2 rounded-full hover:bg-card-hover transition-colors text-muted-foreground hover:text-foreground"
        aria-label="Add label"
      >
        <Tag className="w-4 h-4" />
      </motion.button>

      {typeof window !== "undefined" &&
        createPortal(
          <AnimatePresence>
            {isOpen && (
              <motion.div
                ref={dropdownRef}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.15 }}
                onClick={(e) => e.stopPropagation()}
                style={{
                  position: "fixed",
                  top: dropdownPosition.top,
                  left: dropdownPosition.left,
                  transform: "translateY(-100%)",
                }}
                className="w-56 bg-card border border-card-border rounded-lg shadow-lg overflow-hidden z-[9999]"
              >
                <div className="p-2 border-b border-card-border">
                  <span className="text-xs font-medium text-muted-foreground">Label note</span>
                </div>

                <div className="max-h-48 overflow-y-auto">
                  {labels.length === 0 ? (
                    <div className="p-3 text-sm text-muted-foreground text-center">
                      No labels yet
                    </div>
                  ) : (
                    labels.map((label) => {
                      const isAssigned = taskLabels.includes(label.id);
                      return (
                        <button
                          key={label.id}
                          onClick={() => handleToggleLabel(label.id)}
                          disabled={loading}
                          className="w-full flex items-center gap-3 px-3 py-2 hover:bg-card-hover transition-colors text-left disabled:opacity-50"
                        >
                          <div
                            className={`w-5 h-5 rounded border flex items-center justify-center transition-colors ${
                              isAssigned
                                ? "bg-primary border-primary"
                                : "border-muted-foreground"
                            }`}
                          >
                            {isAssigned && <Check className="w-3 h-3 text-primary-foreground" />}
                          </div>
                          <span className="text-sm text-foreground">{label.name}</span>
                        </button>
                      );
                    })
                  )}
                </div>

                {/* Create new label */}
                <div className="border-t border-card-border">
                  {showNewLabelInput ? (
                    <div className="p-2 flex items-center gap-2">
                      <input
                        ref={inputRef}
                        type="text"
                        value={newLabelName}
                        onChange={(e) => setNewLabelName(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            handleCreateLabel();
                          } else if (e.key === "Escape") {
                            setShowNewLabelInput(false);
                            setNewLabelName("");
                          }
                        }}
                        placeholder="Enter label name"
                        maxLength={50}
                        className="flex-1 text-sm bg-transparent border-b border-primary focus:outline-none text-foreground placeholder:text-muted-foreground"
                      />
                      <button
                        onClick={handleCreateLabel}
                        disabled={!newLabelName.trim() || loading}
                        className="text-xs text-primary hover:text-primary/80 disabled:opacity-50"
                      >
                        Done
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => setShowNewLabelInput(true)}
                      className="w-full flex items-center gap-2 px-3 py-2 hover:bg-card-hover transition-colors text-sm text-muted-foreground hover:text-foreground"
                    >
                      <Plus className="w-4 h-4" />
                      <span>Create label</span>
                    </button>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>,
          document.body
        )}
    </div>
  );
}
