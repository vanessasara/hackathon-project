"use client";

import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronLeft, ChevronRight, Download } from "lucide-react";
import type { TaskImage } from "@/types";

interface ImageViewerProps {
  image: TaskImage;
  onClose: () => void;
  onPrevious?: () => void;
  onNext?: () => void;
  currentIndex?: number;
  totalCount?: number;
}

export function ImageViewer({
  image,
  onClose,
  onPrevious,
  onNext,
  currentIndex,
  totalCount,
}: ImageViewerProps) {
  // Handle keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      switch (e.key) {
        case "Escape":
          onClose();
          break;
        case "ArrowLeft":
          onPrevious?.();
          break;
        case "ArrowRight":
          onNext?.();
          break;
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose, onPrevious, onNext]);

  // Prevent body scroll when viewer is open
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = image.url;
    link.download = image.filename;
    link.target = "_blank";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] bg-black/90 flex items-center justify-center"
        onClick={onClose}
      >
        {/* Close button */}
        <motion.button
          type="button"
          onClick={onClose}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="absolute top-4 right-4 p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
          aria-label="Close"
        >
          <X className="w-6 h-6" />
        </motion.button>

        {/* Download button */}
        <motion.button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            handleDownload();
          }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="absolute top-4 right-16 p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
          aria-label="Download"
        >
          <Download className="w-6 h-6" />
        </motion.button>

        {/* Previous button */}
        {onPrevious && (
          <motion.button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onPrevious();
            }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="absolute left-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
            aria-label="Previous"
          >
            <ChevronLeft className="w-8 h-8" />
          </motion.button>
        )}

        {/* Next button */}
        {onNext && (
          <motion.button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onNext();
            }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="absolute right-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
            aria-label="Next"
          >
            <ChevronRight className="w-8 h-8" />
          </motion.button>
        )}

        {/* Image */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="max-w-[90vw] max-h-[85vh]"
          onClick={(e) => e.stopPropagation()}
        >
          <img
            src={image.url}
            alt={image.filename}
            className="max-w-full max-h-[85vh] object-contain rounded"
          />
        </motion.div>

        {/* Counter */}
        {totalCount !== undefined && totalCount > 1 && currentIndex !== undefined && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-white/10 text-white text-sm">
            {currentIndex + 1} / {totalCount}
          </div>
        )}

        {/* Filename */}
        <div className="absolute bottom-4 left-4 text-white/70 text-sm truncate max-w-xs">
          {image.filename}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
