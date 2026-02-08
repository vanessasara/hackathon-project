"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { LogOut, User } from "lucide-react";
import { signOut } from "@/lib/auth-client";

interface UserMenuProps {
  userEmail: string;
}

export function UserMenu({ userEmail }: UserMenuProps) {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Get user initials from email
  const getInitials = (email: string) => {
    const name = email.split("@")[0];
    if (name.length >= 2) {
      return name.slice(0, 2).toUpperCase();
    }
    return name.toUpperCase();
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };

    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, []);

  const handleLogout = async () => {
    setLoading(true);
    try {
      await signOut({
        fetchOptions: {
          onSuccess: () => {
            router.push("/login");
          },
        },
      });
    } catch (error) {
      // Session might already be cleared or network issue
      // Still redirect to login page
      console.error("Logout error:", error);
      router.push("/login");
    }
  };

  return (
    <div className="relative" ref={menuRef}>
      {/* Avatar button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center text-indigo-700 dark:text-indigo-400 font-bold text-sm hover:from-indigo-500/30 hover:to-violet-500/30 transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500/50 ring-2 ring-indigo-500/20"
        aria-label="User menu"
        aria-expanded={isOpen}
      >
        {getInitials(userEmail)}
      </motion.button>

      {/* Dropdown menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 mt-2 w-72 bg-card rounded-xl border border-card-border shadow-lg overflow-hidden z-50"
          >
            {/* User info section */}
            <div className="p-4 border-b border-card-border bg-gradient-to-br from-indigo-500/5 to-violet-500/5">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500/30 to-violet-500/30 flex items-center justify-center text-indigo-700 dark:text-indigo-300 font-bold text-lg ring-2 ring-indigo-500/30">
                  {getInitials(userEmail)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">
                    {userEmail.split("@")[0]}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">
                    {userEmail}
                  </p>
                </div>
              </div>
            </div>

            {/* Menu items */}
            <div className="p-2">
              <button
                onClick={handleLogout}
                disabled={loading}
                className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-foreground hover:bg-card-hover rounded-lg transition-colors disabled:opacity-50"
              >
                <LogOut className="w-4 h-4 text-muted-foreground" />
                <span>{loading ? "Signing out..." : "Sign out"}</span>
              </button>
            </div>

            {/* Footer */}
            <div className="px-4 py-3 border-t border-card-border bg-sidebar-bg/50">
              <p className="text-xs font-medium bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent text-center">
                Velocity - Move with purpose
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
