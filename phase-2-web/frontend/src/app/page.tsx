import { redirect } from "next/navigation";
import { getSession } from "./proxy";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default async function HomePage() {
  const session = await getSession();

  // Redirect authenticated users to dashboard
  if (session) {
    redirect("/dashboard");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center max-w-2xl mx-auto px-4">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Todo App
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          A simple, powerful task management application.
          Create, organize, and complete your tasks with ease.
        </p>
        <div className="flex gap-4 justify-center flex-col sm:flex-row">
          <Link href="/login">
            <Button size="lg" className="w-full sm:w-auto">Sign In</Button>
          </Link>
          <Link href="/register">
            <Button variant="secondary" size="lg" className="w-full sm:w-auto">Create Account</Button>
          </Link>
        </div>
        <p className="mt-8 text-sm text-gray-500">
          Built with Next.js, FastAPI, and PostgreSQL
        </p>
      </div>
    </div>
  );
}
