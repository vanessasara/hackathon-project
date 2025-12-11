"use client";

import { motion } from "framer-motion";
import { LayoutGrid, List } from "lucide-react";

export type ViewMode = "grid" | "list";

interface ViewToggleProps {
  viewMode: ViewMode;
  onViewChange: (mode: ViewMode) => void;
}

export function ViewToggle({ viewMode, onViewChange }: ViewToggleProps) {
  return (
    <motion.button
      onClick={() => onViewChange(viewMode === "grid" ? "list" : "grid")}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      className="p-2 rounded-full hover:bg-card-hover transition-colors"
      aria-label={`Switch to ${viewMode === "grid" ? "list" : "grid"} view`}
    >
      {viewMode === "grid" ? (
        <List className="w-5 h-5 text-muted-foreground" />
      ) : (
        <LayoutGrid className="w-5 h-5 text-muted-foreground" />
      )}
    </motion.button>
  );
}
