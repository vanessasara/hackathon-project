"use client";

import { useRouter } from "next/navigation";
import { signOut } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export function LogoutButton() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

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
    <Button
      onClick={handleLogout}
      variant="secondary"
      size="sm"
      disabled={loading}
    >
      {loading ? "Signing out..." : "Sign Out"}
    </Button>
  );
}
