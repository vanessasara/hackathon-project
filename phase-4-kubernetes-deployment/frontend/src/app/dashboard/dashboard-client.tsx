"use client";

import { useState, createContext, useContext } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Menu, Search, Settings, RefreshCw } from "lucide-react";
import { Sidebar } from "@/components/sidebar";
import { ThemeToggle } from "@/components/theme-toggle";
import { ViewToggle, ViewMode } from "@/components/view-toggle";
import { UserMenu } from "@/components/user-menu";
import { EditLabelsModal } from "@/components/edit-labels-modal";

// Context for sharing view mode across components
interface DashboardContextType {
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error("useDashboard must be used within DashboardClient");
  }
  return context;
}

interface DashboardClientProps {
  children: React.ReactNode;
  userEmail: string;
}

export function DashboardClient({ children, userEmail }: DashboardClientProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [viewMode, setViewMode] = useState<ViewMode>("grid");
  const [editLabelsOpen, setEditLabelsOpen] = useState(false);

  return (
    <DashboardContext.Provider
      value={{ viewMode, setViewMode, sidebarOpen, setSidebarOpen }}
    >
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="fixed top-0 left-0 right-0 z-40 bg-background border-b border-border">
          <div className="flex items-center justify-between px-2 py-2 lg:px-4">
            {/* Left section */}
            <div className="flex items-center gap-1">
              <motion.button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="p-3 rounded-full hover:bg-card-hover transition-colors"
                aria-label="Toggle sidebar"
              >
                <Menu className="w-6 h-6 text-muted-foreground" />
              </motion.button>
              <Link
                href="/dashboard"
                className="flex items-center gap-2 px-2"
              >
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-amber-500 flex items-center justify-center shadow-sm">
                  <svg className="w-6 h-6 text-primary-foreground" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M9 11l3 3L22 4" />
                    <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
                  </svg>
                </div>
                <span className="text-xl font-semibold text-foreground hidden sm:inline">
                  Notely
                </span>
              </Link>
            </div>

            {/* Center - Search bar */}
            <div className="flex-1 max-w-2xl mx-4 hidden md:block">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search"
                  className="w-full pl-12 pr-4 py-3 bg-input-bg rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            {/* Right section */}
            <div className="flex items-center gap-1">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-full hover:bg-card-hover transition-colors hidden sm:flex"
                aria-label="Refresh"
              >
                <RefreshCw className="w-5 h-5 text-muted-foreground" />
              </motion.button>
              <ViewToggle viewMode={viewMode} onViewChange={setViewMode} />
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-full hover:bg-card-hover transition-colors hidden sm:flex"
                aria-label="Settings"
              >
                <Settings className="w-5 h-5 text-muted-foreground" />
              </motion.button>
              <ThemeToggle />
              <UserMenu userEmail={userEmail} />
            </div>
          </div>
        </header>

        {/* Main content area */}
        <div className="flex pt-16">
          {/* Sidebar */}
          <Sidebar
            isOpen={sidebarOpen}
            onToggle={() => setSidebarOpen(!sidebarOpen)}
            onEditLabels={() => setEditLabelsOpen(true)}
          />

          {/* Main content */}
          <main
            className={`
              flex-1 transition-all duration-300 ease-in-out
              ${sidebarOpen ? "lg:ml-0" : "lg:ml-0"}
              p-4 lg:p-8
            `}
          >
            {children}
          </main>
        </div>

        {/* Edit Labels Modal */}
        <EditLabelsModal
          isOpen={editLabelsOpen}
          onClose={() => setEditLabelsOpen(false)}
        />
      </div>
    </DashboardContext.Provider>
  );
}
