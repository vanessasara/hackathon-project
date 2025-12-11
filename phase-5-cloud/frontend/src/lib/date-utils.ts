/**
 * Date utility functions for handling time in the todo app.
 *
 * The backend stores datetimes in UTC. All times sent to the backend
 * should be in ISO 8601 UTC format.
 */

/**
 * Format a Date object as an ISO string in UTC.
 * The backend expects UTC time for proper timezone handling.
 *
 * Example: If user is in UTC+5 and selects 8:00 AM local:
 * - toLocalISOString() returns "2025-12-05T03:00:00.000Z" (UTC)
 * - Backend stores this as UTC
 * - When displayed, it converts back to user's local time
 */
export function toLocalISOString(date: Date): string {
  return date.toISOString();
}

/**
 * Parse a date string from the backend as UTC.
 * Backend returns dates without timezone suffix, but stores in UTC.
 */
export function parseUTCDate(dateStr: string): Date {
  // If the date string doesn't have a timezone indicator, treat it as UTC
  if (!dateStr.endsWith('Z') && !dateStr.includes('+') && !dateStr.includes('-', 10)) {
    return new Date(dateStr + 'Z');
  }
  return new Date(dateStr);
}

/**
 * Format a reminder date string for display.
 * Shows "Today", "Tomorrow", or the date with time.
 */
export function formatReminderDate(dateStr: string): string {
  const date = parseUTCDate(dateStr);
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
