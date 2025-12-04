/**
 * Date utility functions for handling local time in the todo app.
 *
 * The backend stores datetimes as naive (no timezone), so we need to
 * send local time directly without UTC conversion.
 */

/**
 * Format a Date object as an ISO-like string in LOCAL time.
 * This prevents the UTC conversion that toISOString() does.
 *
 * Example: If user is in UTC+5 and selects 8:00 AM:
 * - toISOString() would return "2025-12-05T03:00:00.000Z" (UTC)
 * - toLocalISOString() returns "2025-12-05T08:00:00" (local time preserved)
 */
export function toLocalISOString(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}

/**
 * Format a reminder date string for display.
 * Shows "Today", "Tomorrow", or the date with time.
 */
export function formatReminderDate(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const isToday = date.toDateString() === now.toDateString();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  const isTomorrow = date.toDateString() === tomorrow.toDateString();

  const timeStr = date.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });

  if (isToday) return `Today, ${timeStr}`;
  if (isTomorrow) return `Tomorrow, ${timeStr}`;
  return date.toLocaleDateString([], {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}
