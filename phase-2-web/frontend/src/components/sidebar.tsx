"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Lightbulb,
  Bell,
  Pencil,
  Archive,
  Trash2,
  Menu,
  Tag,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import { Label } from "@/types";
import { labelsApi } from "@/lib/api";
import { getToken, useSession } from "@/lib/auth-client";

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  onEditLabels?: () => void;
}

interface NavItem {
  icon: React.ElementType;
  label: string;
  href: string;
  isAction?: boolean;
  onClick?: () => void;
}

export function Sidebar({ isOpen, onToggle, onEditLabels }: SidebarProps) {
  const pathname = usePathname();
  const { data: session } = useSession();
  const [labels, setLabels] = useState<Label[]>([]);
  const [labelsExpanded, setLabelsExpanded] = useState(true);

  useEffect(() => {
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

    if (session?.user) {
      fetchLabels();
    }
  }, [session]);

  const mainNavItems: NavItem[] = [
    { icon: Lightbulb, label: "Notes", href: "/dashboard" },
    { icon: Bell, label: "Reminders", href: "/dashboard/reminders" },
  ];

  const bottomNavItems: NavItem[] = [
    {
      icon: Pencil,
      label: "Edit labels",
      href: "#",
      isAction: true,
      onClick: onEditLabels,
    },
    { icon: Archive, label: "Archive", href: "/dashboard/archive" },
    { icon: Trash2, label: "Trash", href: "/dashboard/trash" },
  ];

  const isActive = (href: string) => {
    if (href === "/dashboard") {
      return pathname === "/dashboard";
    }
    return pathname?.startsWith(href);
  };

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onToggle}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: isOpen ? 280 : 72 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className={`
          fixed left-0 top-16 bottom-0 z-50
          bg-sidebar-bg
          flex flex-col overflow-hidden
          lg:relative lg:top-0
          ${!isOpen && "hidden lg:flex"}
        `}
      >
        <nav className="flex-1 py-2 overflow-y-auto overflow-x-hidden">
          {/* Main nav items */}
          {mainNavItems.map((item) => (
            <NavButton
              key={item.label}
              item={item}
              isExpanded={isOpen}
              isActive={isActive(item.href)}
            />
          ))}

          {/* Labels section */}
          {labels.length > 0 && (
            <div className="mt-2">
              {isOpen && (
                <button
                  onClick={() => setLabelsExpanded(!labelsExpanded)}
                  className="flex items-center gap-2 px-6 py-2 w-full text-left text-xs font-medium uppercase tracking-wider text-muted-foreground hover:text-foreground transition-colors"
                >
                  {labelsExpanded ? (
                    <ChevronDown className="w-3 h-3" />
                  ) : (
                    <ChevronRight className="w-3 h-3" />
                  )}
                  Labels
                </button>
              )}
              <AnimatePresence>
                {(labelsExpanded || !isOpen) &&
                  labels.map((label) => (
                    <motion.div
                      key={label.id}
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                    >
                      <NavButton
                        item={{
                          icon: Tag,
                          label: label.name,
                          href: `/dashboard/labels/${label.id}`,
                        }}
                        isExpanded={isOpen}
                        isActive={pathname === `/dashboard/labels/${label.id}`}
                      />
                    </motion.div>
                  ))}
              </AnimatePresence>
            </div>
          )}

          {/* Divider */}
          <div className="my-2 mx-6 border-t border-border" />

          {/* Bottom nav items */}
          {bottomNavItems.map((item) => (
            <NavButton
              key={item.label}
              item={item}
              isExpanded={isOpen}
              isActive={isActive(item.href)}
            />
          ))}
        </nav>
      </motion.aside>
    </>
  );
}

function NavButton({
  item,
  isExpanded,
  isActive,
}: {
  item: NavItem;
  isExpanded: boolean;
  isActive: boolean;
}) {
  const Icon = item.icon;

  const className = `
    flex items-center gap-5 px-3 py-3 mr-3 mb-1 rounded-r-full
    transition-colors cursor-pointer w-full text-left
    ${
      isActive
        ? "bg-sidebar-active text-foreground"
        : "text-muted-foreground hover:bg-sidebar-hover"
    }
  `;

  const content = (
    <>
      <Icon className="w-5 h-5 flex-shrink-0 ml-3" />
      <AnimatePresence>
        {isExpanded && (
          <motion.span
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: "auto" }}
            exit={{ opacity: 0, width: 0 }}
            className="text-sm font-medium whitespace-nowrap overflow-hidden"
          >
            {item.label}
          </motion.span>
        )}
      </AnimatePresence>
    </>
  );

  if (item.isAction && item.onClick) {
    return (
      <button onClick={item.onClick} className={className}>
        {content}
      </button>
    );
  }

  return (
    <Link href={item.href} className={className}>
      {content}
    </Link>
  );
}

export function SidebarToggle({ onToggle }: { onToggle: () => void }) {
  return (
    <motion.button
      onClick={onToggle}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      className="p-2 rounded-full hover:bg-card-hover transition-colors"
      aria-label="Toggle sidebar"
    >
      <Menu className="w-6 h-6 text-muted-foreground" />
    </motion.button>
  );
}
