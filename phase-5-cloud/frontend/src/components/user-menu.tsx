"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { LogOut, Bell, BellOff, AlertCircle, RefreshCw } from "lucide-react";
import { signOut, getToken } from "@/lib/auth-client";
import {
  isPushSupported,
  initializePushNotifications,
  NotificationResult,
} from "@/lib/notifications";

interface UserMenuProps {
  userEmail: string;
}

type NotificationState = 'idle' | 'enabling' | 'enabled' | 'error';

export function UserMenu({ userEmail }: UserMenuProps) {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notificationsSupported, setNotificationsSupported] = useState(false);
  const [notificationState, setNotificationState] = useState<NotificationState>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  // Check notification support on mount
  // DO NOT auto-enable based on browser permission - always let user click
  useEffect(() => {
    if (typeof window !== "undefined") {
      setNotificationsSupported(isPushSupported());
    }
  }, []);

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

  const handleEnableNotifications = async () => {
    // Clear previous error
    setErrorMessage(null);

    // Get auth token first
    const { data: tokenData, error: tokenError } = await getToken();

    if (tokenError || !tokenData?.token) {
      console.error("No auth token available");
      setNotificationState('error');
      setErrorMessage("Please log in again to enable notifications");
      return;
    }

    setNotificationState('enabling');

    try {
      const result: NotificationResult = await initializePushNotifications(tokenData.token);

      if (result.success) {
        setNotificationState('enabled');
        setErrorMessage(null);
        console.log("Push notifications enabled successfully");
      } else {
        setNotificationState('error');
        setErrorMessage(result.error || "Failed to enable notifications");
        console.error("Failed to enable push notifications:", result.error, "at step:", result.step);
      }
    } catch (error) {
      console.error("Error enabling notifications:", error);
      setNotificationState('error');
      setErrorMessage("Unexpected error. Please try again.");
    }
  };

  // Render the notification button based on current state
  const renderNotificationButton = () => {
    if (!notificationsSupported) {
      return null;
    }

    const isEnabling = notificationState === 'enabling';
    const isEnabled = notificationState === 'enabled';
    const hasError = notificationState === 'error';

    return (
      <div className="space-y-1">
        <button
          onClick={handleEnableNotifications}
          disabled={isEnabling}
          className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-foreground hover:bg-card-hover rounded-lg transition-colors disabled:opacity-50"
        >
          {isEnabled ? (
            <>
              <Bell className="w-4 h-4 text-green-500" />
              <span className="flex-1 text-left">Notifications enabled</span>
              <RefreshCw className="w-3 h-3 text-muted-foreground" />
            </>
          ) : hasError ? (
            <>
              <AlertCircle className="w-4 h-4 text-destructive" />
              <span className="flex-1 text-left">Retry notifications</span>
            </>
          ) : isEnabling ? (
            <>
              <Bell className="w-4 h-4 text-muted-foreground animate-pulse" />
              <span>Enabling...</span>
            </>
          ) : (
            <>
              <BellOff className="w-4 h-4 text-muted-foreground" />
              <span>Enable notifications</span>
            </>
          )}
        </button>

        {/* Show error message if any */}
        {hasError && errorMessage && (
          <p className="px-3 text-xs text-destructive">
            {errorMessage}
          </p>
        )}

        {/* Show hint for enabled state */}
        {isEnabled && (
          <p className="px-3 text-xs text-muted-foreground">
            Click to re-sync subscription
          </p>
        )}
      </div>
    );
  };

  return (
    <div className="relative" ref={menuRef}>
      {/* Avatar button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center text-primary font-medium text-sm hover:bg-primary/30 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
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
            <div className="p-4 border-b border-card-border">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary font-semibold text-lg">
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
            <div className="p-2 space-y-1">
              {/* Notification toggle */}
              {renderNotificationButton()}

              {/* Logout */}
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
              <p className="text-xs text-muted-foreground text-center">
                Notely - Your personal task manager
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
