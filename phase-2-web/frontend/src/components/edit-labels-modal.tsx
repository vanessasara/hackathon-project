"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, Tag, Trash2, Check, Pencil } from "lucide-react";
import { Label } from "@/types";
import { labelsApi } from "@/lib/api";
import { getToken, useSession } from "@/lib/auth-client";

interface EditLabelsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function EditLabelsModal({ isOpen, onClose }: EditLabelsModalProps) {
  const { data: session } = useSession();
  const [labels, setLabels] = useState<Label[]>([]);
  const [newLabelName, setNewLabelName] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingName, setEditingName] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const fetchLabels = async () => {
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      const data = await labelsApi.list(tokenData.token);
      setLabels(data);
    } catch (err) {
      console.error("Failed to fetch labels:", err);
    }
  };

  useEffect(() => {
    if (isOpen && session?.user) {
      fetchLabels();
    }
  }, [isOpen, session]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleCreateLabel = async () => {
    if (!newLabelName.trim()) return;

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setLoading(true);
    try {
      await labelsApi.create(tokenData.token, { name: newLabelName.trim() });
      setNewLabelName("");
      fetchLabels();
    } catch (err) {
      console.error("Failed to create label:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateLabel = async (id: number) => {
    if (!editingName.trim()) {
      setEditingId(null);
      return;
    }

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await labelsApi.update(tokenData.token, id, { name: editingName.trim() });
      setEditingId(null);
      fetchLabels();
    } catch (err) {
      console.error("Failed to update label:", err);
    }
  };

  const handleDeleteLabel = async (id: number) => {
    if (!confirm("Delete this label? Notes won't be deleted.")) return;

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    try {
      await labelsApi.delete(tokenData.token, id);
      fetchLabels();
    } catch (err) {
      console.error("Failed to delete label:", err);
    }
  };

  const startEditing = (label: Label) => {
    setEditingId(label.id);
    setEditingName(label.name);
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
          className="bg-card rounded-lg shadow-xl w-full max-w-sm overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-border">
            <h2 className="text-lg font-medium">Edit labels</h2>
            <button
              onClick={onClose}
              className="p-1 rounded-full hover:bg-card-hover transition-colors"
            >
              <X className="w-5 h-5 text-muted-foreground" />
            </button>
          </div>

          {/* Create new label */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
            <button
              onClick={handleCreateLabel}
              disabled={loading || !newLabelName.trim()}
              className="p-1 rounded-full hover:bg-card-hover transition-colors disabled:opacity-50"
            >
              <Plus className="w-5 h-5 text-muted-foreground" />
            </button>
            <input
              ref={inputRef}
              type="text"
              value={newLabelName}
              onChange={(e) => setNewLabelName(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleCreateLabel()}
              placeholder="Create new label"
              className="flex-1 bg-transparent text-foreground placeholder:text-muted-foreground focus:outline-none"
            />
            {newLabelName.trim() && (
              <button
                onClick={handleCreateLabel}
                disabled={loading}
                className="p-1 rounded-full hover:bg-card-hover transition-colors"
              >
                <Check className="w-5 h-5 text-primary" />
              </button>
            )}
          </div>

          {/* Labels list */}
          <div className="max-h-64 overflow-y-auto">
            {labels.length === 0 ? (
              <div className="px-4 py-8 text-center text-muted-foreground">
                <Tag className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">No labels yet</p>
              </div>
            ) : (
              labels.map((label) => (
                <div
                  key={label.id}
                  className="flex items-center gap-3 px-4 py-2 hover:bg-card-hover transition-colors group"
                >
                  {editingId === label.id ? (
                    <>
                      <Tag className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                      <input
                        type="text"
                        value={editingName}
                        onChange={(e) => setEditingName(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") handleUpdateLabel(label.id);
                          if (e.key === "Escape") setEditingId(null);
                        }}
                        onBlur={() => handleUpdateLabel(label.id)}
                        autoFocus
                        className="flex-1 bg-transparent text-foreground focus:outline-none border-b border-primary"
                      />
                      <button
                        onClick={() => handleUpdateLabel(label.id)}
                        className="p-1 rounded-full hover:bg-card-hover transition-colors"
                      >
                        <Check className="w-5 h-5 text-primary" />
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => handleDeleteLabel(label.id)}
                        className="p-1 rounded-full hover:bg-destructive/20 transition-colors opacity-0 group-hover:opacity-100"
                      >
                        <Trash2 className="w-4 h-4 text-destructive" />
                      </button>
                      <Tag className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                      <span className="flex-1 text-foreground truncate">
                        {label.name}
                      </span>
                      <button
                        onClick={() => startEditing(label)}
                        className="p-1 rounded-full hover:bg-card-hover transition-colors opacity-0 group-hover:opacity-100"
                      >
                        <Pencil className="w-4 h-4 text-muted-foreground" />
                      </button>
                    </>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="flex justify-end px-4 py-3 border-t border-border">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-foreground hover:bg-card-hover rounded-lg transition-colors"
            >
              Done
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
