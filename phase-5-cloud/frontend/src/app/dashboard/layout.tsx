import { redirect } from "next/navigation";
import { getSession } from "../proxy";
import { DashboardClient } from "./dashboard-client";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getSession();

  if (!session) {
    redirect("/login");
  }

  return <DashboardClient userEmail={session.user.email}>{children}</DashboardClient>;
}
