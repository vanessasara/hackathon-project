"use client";

import { motion } from "framer-motion";
import { useTheme } from "next-themes";
import { Check, Palette } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { KEEP_COLORS, COLOR_KEYS, ColorKey, getColor } from "@/lib/colors";

interface ColorPickerProps {
  selectedColor: ColorKey;
  onColorChange: (color: ColorKey) => void;
  size?: "sm" | "md";
}

export function ColorPicker({
  selectedColor,
  onColorChange,
  size = "md",
}: ColorPickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";
  const ref = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const buttonSize = size === "sm" ? "w-6 h-6" : "w-8 h-8";
  const dotSize = size === "sm" ? "w-6 h-6" : "w-8 h-8";

  return (
    <div className="relative" ref={ref}>
      <motion.button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        className={`${buttonSize} rounded-full flex items-center justify-center hover:bg-card-hover transition-colors`}
        aria-label="Choose color"
      >
        <Palette className="w-4 h-4 text-muted-foreground" />
      </motion.button>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: -10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: -10 }}
          className="absolute bottom-full mb-2 left-0 p-3 bg-card rounded-lg shadow-lg border border-border z-50 min-w-[160px]"
        >
          <div className="grid grid-cols-4 gap-2">
            {COLOR_KEYS.map((colorKey) => {
              const color = getColor(colorKey, isDark);
              const isSelected = selectedColor === colorKey;
              const isDefault = colorKey === "default";

              return (
                <motion.button
                  key={colorKey}
                  type="button"
                  onClick={() => {
                    onColorChange(colorKey);
                    setIsOpen(false);
                  }}
                  whileHover={{ scale: 1.15 }}
                  whileTap={{ scale: 0.95 }}
                  className={`
                    ${dotSize} rounded-full flex items-center justify-center
                    ${isDefault ? "border-2 border-dashed border-border" : ""}
                    ${isSelected && !isDefault ? "ring-2 ring-primary ring-offset-2 ring-offset-card" : ""}
                  `}
                  style={{
                    backgroundColor: isDefault ? "transparent" : color,
                  }}
                  aria-label={colorKey}
                >
                  {isSelected && (
                    <Check
                      className={`w-4 h-4 ${
                        isDefault || isDark ? "text-foreground" : "text-gray-700"
                      }`}
                    />
                  )}
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
}

// Inline color strip for toolbar
export function ColorStrip({
  selectedColor,
  onColorChange,
}: Omit<ColorPickerProps, "size">) {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  return (
    <div className="flex items-center gap-1">
      {COLOR_KEYS.slice(0, 6).map((colorKey) => {
        const color = getColor(colorKey, isDark);
        const isSelected = selectedColor === colorKey;
        const isDefault = colorKey === "default";

        return (
          <motion.button
            key={colorKey}
            type="button"
            onClick={() => onColorChange(colorKey)}
            whileHover={{ scale: 1.2 }}
            whileTap={{ scale: 0.9 }}
            className={`
              w-6 h-6 rounded-full
              ${isDefault ? "border-2 border-dashed border-border" : ""}
              ${isSelected ? "ring-2 ring-primary" : ""}
            `}
            style={{
              backgroundColor: isDefault ? "transparent" : color,
            }}
            aria-label={colorKey}
          />
        );
      })}
    </div>
  );
}
