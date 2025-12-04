"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { ImagePlus, Loader2 } from "lucide-react";
import { imagesApi } from "@/lib/api";
import { getToken } from "@/lib/auth-client";
import type { TaskImage } from "@/types";

interface ImageUploadProps {
  taskId: number;
  onUpload: (image: TaskImage) => void;
  size?: "sm" | "md";
}

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

export function ImageUpload({ taskId, onUpload, size = "sm" }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Reset
    setError(null);

    // Validate file type
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError("Invalid file type. Use JPEG, PNG, GIF, or WebP.");
      return;
    }

    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
      setError("File too large. Maximum size is 5MB.");
      return;
    }

    // Get token
    const { data: tokenData, error: tokenError } = await getToken();
    if (tokenError || !tokenData?.token) {
      setError("Authentication required");
      return;
    }

    // Upload
    setUploading(true);
    try {
      const image = await imagesApi.upload(tokenData.token, taskId, file);
      onUpload(image);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const iconSize = size === "sm" ? "w-4 h-4" : "w-5 h-5";
  const buttonSize = size === "sm" ? "p-2" : "p-2.5";

  return (
    <div className="relative">
      <input
        ref={fileInputRef}
        type="file"
        accept={ALLOWED_TYPES.join(",")}
        onChange={handleFileChange}
        className="hidden"
      />
      <motion.button
        type="button"
        onClick={handleClick}
        disabled={uploading}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        className={`${buttonSize} rounded-full text-muted-foreground hover:text-foreground hover:bg-card-hover transition-colors disabled:opacity-50`}
        aria-label="Add image"
        title={error || "Add image"}
      >
        {uploading ? (
          <Loader2 className={`${iconSize} animate-spin`} />
        ) : (
          <ImagePlus className={iconSize} />
        )}
      </motion.button>
      {error && (
        <div className="absolute top-full left-0 mt-1 text-xs text-destructive whitespace-nowrap z-10 bg-card px-2 py-1 rounded shadow">
          {error}
        </div>
      )}
    </div>
  );
}
