"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { CheckCircle2, Sparkles, Zap, Shield } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";

const features = [
  {
    icon: CheckCircle2,
    title: "Simple & Intuitive",
    description: "Create and manage tasks with just a few clicks",
  },
  {
    icon: Sparkles,
    title: "Beautiful Design",
    description: "Modern UI with dark and light themes",
  },
  {
    icon: Zap,
    title: "Fast & Responsive",
    description: "Built with Next.js for blazing-fast performance",
  },
  {
    icon: Shield,
    title: "Secure",
    description: "Your data is protected with industry-standard security",
  },
];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between p-4 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-amber-500 flex items-center justify-center shadow-sm">
            <svg className="w-6 h-6 text-primary-foreground" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
            </svg>
          </div>
          <span className="text-xl font-semibold text-foreground">Notely</span>
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <Link
            href="/login"
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-medium"
          >
            Get Started
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-8"
          >
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-foreground">
              Your personal task manager
            </span>
          </motion.div>

          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
            Capture ideas,{" "}
            <span className="text-primary">organize tasks</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            A beautiful, simple task management app.
            Create notes, organize your thoughts, and get things done.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/register"
                className="inline-flex items-center justify-center px-8 py-4 bg-primary text-primary-foreground rounded-xl text-lg font-semibold shadow-lg shadow-primary/25 hover:bg-primary/90 transition-colors"
              >
                Start for free
              </Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/login"
                className="inline-flex items-center justify-center px-8 py-4 bg-card border border-card-border text-foreground rounded-xl text-lg font-semibold hover:bg-card-hover transition-colors"
              >
                Sign in
              </Link>
            </motion.div>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-24 max-w-6xl mx-auto"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              className="p-6 bg-card rounded-xl border border-card-border hover:shadow-lg transition-shadow"
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Demo preview placeholder */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="mt-24 w-full max-w-4xl mx-auto"
        >
          <div className="relative">
            {/* Browser frame */}
            <div className="bg-card rounded-xl border border-card-border shadow-2xl overflow-hidden">
              {/* Browser header */}
              <div className="flex items-center gap-2 px-4 py-3 border-b border-card-border bg-sidebar-bg">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                  <div className="w-3 h-3 rounded-full bg-green-500/80" />
                </div>
                <div className="flex-1 ml-4">
                  <div className="w-64 h-6 bg-input-bg rounded-md" />
                </div>
              </div>
              {/* Content preview */}
              <div className="p-8 grid grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="rounded-lg p-4 h-32"
                    style={{
                      backgroundColor: [
                        "var(--color-coral)",
                        "var(--color-sand)",
                        "var(--color-mint)",
                        "var(--color-fog)",
                        "var(--color-dusk)",
                        "var(--color-peach)",
                      ][i] || "var(--card)",
                    }}
                  >
                    <div className="w-20 h-3 bg-black/10 rounded mb-2" />
                    <div className="w-full h-2 bg-black/10 rounded mb-1" />
                    <div className="w-3/4 h-2 bg-black/10 rounded" />
                  </div>
                ))}
              </div>
            </div>
            {/* Glow effect */}
            <div className="absolute -inset-4 bg-gradient-to-r from-primary/20 via-amber-500/20 to-primary/20 rounded-2xl blur-3xl -z-10" />
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center border-t border-card-border">
        <p className="text-muted-foreground">
          Built with Next.js, FastAPI & PostgreSQL
        </p>
      </footer>
    </div>
  );
}
