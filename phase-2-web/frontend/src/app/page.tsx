import { redirect } from "next/navigation";
import { getSession } from "./proxy";
import { LandingPage } from "@/components/landing-page";

export default async function HomePage() {
  const session = await getSession();

  // Redirect authenticated users to dashboard
  if (session) {
    redirect("/dashboard");
  }

  return <LandingPage />;
}
