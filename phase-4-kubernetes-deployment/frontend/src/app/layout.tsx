import type { Metadata } from "next";
import Script from "next/script";
import { ThemeProvider } from "@/lib/theme-provider";
import { Toaster } from "sonner";
import { FloatingChat } from "@/components/chat/FloatingChat";
import "./globals.css";

export const metadata: Metadata = {
  title: "Keep Todo",
  description: "Google Keep-inspired Todo Application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="afterInteractive"
        />
        <ThemeProvider>
          {children}
          <Toaster
            position="bottom-left"
            toastOptions={{
              style: {
                background: "var(--card)",
                border: "1px solid var(--card-border)",
                color: "var(--foreground)",
              },
            }}
          />
          <FloatingChat />
        </ThemeProvider>
      </body>
    </html>
  );
}
