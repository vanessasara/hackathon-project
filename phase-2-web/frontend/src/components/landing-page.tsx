"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { CheckCircle2, Sparkles, Zap, Shield } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";

const features = [
  {
    icon: CheckCircle2,
    title: "Lightning Fast",
    description: "Capture tasks instantly and stay in your flow",
  },
  {
    icon: Sparkles,
    title: "Smart Organization",
    description: "Powerful labels and views to organize your way",
  },
  {
    icon: Zap,
    title: "Built for Speed",
    description: "Blazing-fast performance that keeps up with you",
  },
  {
    icon: Shield,
    title: "Always Secure",
    description: "Enterprise-grade security for your peace of mind",
  },
];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between p-4 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/30 ring-2 ring-indigo-500/20">
            <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 11 12 14 22 4" />
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
            </svg>
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">Velocity</span>
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <Link
            href="/login"
            className="text-muted-foreground hover:text-foreground font-medium transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-violet-600 text-white rounded-lg hover:shadow-lg hover:shadow-indigo-500/40 transition-all font-semibold"
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
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500/10 to-violet-500/10 border border-indigo-500/30 rounded-full mb-8 backdrop-blur-sm"
          >
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span className="text-sm font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
              Move with purpose and velocity
            </span>
          </motion.div>

          {/* Title */}
          <h1 className="text-5xl md:text-7xl font-extrabold text-foreground mb-6 leading-tight tracking-tight">
            Stay focused.{" "}
            <span className="bg-gradient-to-r from-indigo-500 via-violet-500 to-indigo-600 bg-clip-text text-transparent">
              Get things done.
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
            Transform your to-do list into forward momentum. Simple, powerful task management
            that helps you achieve more every day.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/register"
                className="inline-flex items-center justify-center px-10 py-4 bg-gradient-to-r from-indigo-500 to-violet-600 text-white rounded-xl text-lg font-bold shadow-xl shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/50 transition-all ring-2 ring-indigo-500/20"
              >
                Start building momentum
              </Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                href="/login"
                className="inline-flex items-center justify-center px-10 py-4 bg-card border-2 border-indigo-500/30 text-foreground rounded-xl text-lg font-bold hover:bg-indigo-500/5 hover:border-indigo-500/50 transition-all"
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
              className="p-7 bg-card rounded-2xl border-2 border-card-border hover:shadow-xl hover:shadow-indigo-500/10 hover:border-indigo-500/40 hover:-translate-y-1 transition-all duration-300"
            >
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center mb-5 ring-2 ring-indigo-500/20">
                <feature.icon className="w-7 h-7 text-indigo-600" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
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
            <div className="absolute -inset-4 bg-gradient-to-r from-indigo-500/20 via-violet-500/20 to-indigo-500/20 rounded-2xl blur-3xl -z-10" />
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center border-t border-card-border bg-sidebar-bg/30">
        <p className="text-muted-foreground font-medium">
          Built with Next.js, FastAPI & PostgreSQL
        </p>
        <p className="text-xs text-muted-foreground/60 mt-2">
          &copy; 2026 Velocity. Move with purpose.
        </p>
      </footer>
    </div>
  );
}
