"use client";

import React, { useState, useRef, useEffect } from "react";
import { useSession } from "@/lib/auth-client";
import { useChatKit, ChatKit } from "@openai/chatkit-react";

export function FloatingChat() {
  const { data: session } = useSession();
  const [isOpen, setIsOpen] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  // Initialize ChatKit with custom backend
  // The /api/chatkit route in Next.js handles auth header injection
  const chatkit = useChatKit({
    api: {
      url: "/api/chatkit",
      domainKey: "local-dev",
    },
    onError: ({ error }) => {
      console.error("ChatKit error:", error);
    },
  });

  // Handle click outside to close
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (chatRef.current && !chatRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  // Handle task refresh after successful operations
  useEffect(() => {
    const handleRefresh = () => {
      window.dispatchEvent(new CustomEvent("taskCreated"));
    };

    window.addEventListener("chatkit:message", handleRefresh);

    return () => {
      window.removeEventListener("chatkit:message", handleRefresh);
    };
  }, []);

  if (!session) {
    return null;
  }

  return (
    <div ref={chatRef} style={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
      {/* Chat Panel */}
      {isOpen && (
        <div style={{
          width: '380px',
          height: '500px',
          marginBottom: '12px',
          border: '1px solid #e0e0e0',
          borderRadius: '16px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
          backgroundColor: 'white',
          overflow: 'hidden',
        }}>
          <ChatKit control={chatkit.control} />
        </div>
      )}

      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          border: 'none',
          backgroundColor: isOpen ? '#6b7280' : '#3b82f6',
          color: 'white',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.2s ease',
          marginLeft: 'auto',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.05)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
        }}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          // X icon
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        ) : (
          // Chat icon
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        )}
      </button>
    </div>
  );
}
