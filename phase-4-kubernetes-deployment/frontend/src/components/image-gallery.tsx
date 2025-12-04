"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import { imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";
import { ImageViewer } from "./image-viewer";
import type { TaskImage } from "@/types";

interface ImageGalleryProps {
  images: TaskImage[];
  onDelete?: (imageId: number) => void;
  editable?: boolean;
}

export function ImageGallery({ images, onDelete, editable = true }: ImageGalleryProps) {
  const [viewerIndex, setViewerIndex] = useState<number | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  if (images.length === 0) return null;

  const handleDelete = async (e: React.MouseEvent, imageId: number) => {
    e.stopPropagation();
    if (!confirm("Delete this image?")) return;

    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) return;

    setDeletingId(imageId);
    try {
      await imagesApi.delete(tokenData.token, imageId);
      onDelete?.(imageId);
    } catch {
      // Silently fail
    } finally {
      setDeletingId(null);
    }
  };

  const handlePrevious = () => {
    if (viewerIndex !== null && viewerIndex > 0) {
      setViewerIndex(viewerIndex - 1);
    }
  };

  const handleNext = () => {
    if (viewerIndex !== null && viewerIndex < images.length - 1) {
      setViewerIndex(viewerIndex + 1);
    }
  };

  return (
    <>
      <div className="flex flex-wrap gap-2 mt-2">
        {images.map((image, index) => (
          <motion.div
            key={image.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative group"
          >
            <button
              type="button"
              onClick={() => setViewerIndex(index)}
              className="block rounded-md overflow-hidden hover:ring-2 ring-primary transition-all"
            >
              <img
                src={image.url}
                alt={image.filename}
                className="w-20 h-20 object-cover"
                loading="lazy"
              />
            </button>
            {editable && (
              <motion.button
                type="button"
                onClick={(e) => handleDelete(e, image.id)}
                disabled={deletingId === image.id}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="absolute -top-2 -right-2 p-1 rounded-full bg-destructive text-destructive-foreground opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50"
                aria-label="Delete image"
              >
                <X className="w-3 h-3" />
              </motion.button>
            )}
          </motion.div>
        ))}
      </div>

      {/* Full-size viewer */}
      {viewerIndex !== null && (
        <ImageViewer
          image={images[viewerIndex]}
          onClose={() => setViewerIndex(null)}
          onPrevious={viewerIndex > 0 ? handlePrevious : undefined}
          onNext={viewerIndex < images.length - 1 ? handleNext : undefined}
          currentIndex={viewerIndex}
          totalCount={images.length}
        />
      )}
    </>
  );
}
