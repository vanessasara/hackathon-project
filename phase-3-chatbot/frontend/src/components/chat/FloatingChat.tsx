"use client";

import React from "react";
import { useSession } from "@/lib/auth-client";
import { useChatKit, ChatKit } from "@openai/chatkit-react";

export function FloatingChat() {
  const { data: session } = useSession();

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // Initialize ChatKit with custom backend
  const chatkit = useChatKit({
    api: {
      url: `${API_BASE_URL}/api/chatkit`,
      domainKey: "local-dev",
    },
    onError: ({ error }) => {
      console.error("ChatKit error:", error);
    },
  });

  // Log for debugging
  React.useEffect(() => {
    console.log("ChatKit control:", chatkit.control);
    console.log("ChatKit API URL:", `${API_BASE_URL}/api/chatkit`);
  }, [chatkit.control, API_BASE_URL]);

  // Handle task refresh after successful operations
  React.useEffect(() => {
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
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '400px',
      height: '600px',
      zIndex: 1000,
      border: '1px solid #ddd',
      borderRadius: '8px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
      backgroundColor: 'white'
    }}>
      <ChatKit control={chatkit.control} />
    </div>
  );
}
