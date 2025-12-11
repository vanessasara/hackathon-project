/**
 * Service Worker for Todo App Push Notifications
 *
 * Part B: Advanced Features - Browser Push Notifications
 *
 * This service worker handles:
 * - Push notification events from the backend
 * - Notification click events to open the app
 * - Background sync (future)
 */

// Service Worker version for cache management
const SW_VERSION = '1.0.0';

/**
 * Handle push notification events
 *
 * Receives push messages from the server and displays them as notifications
 */
self.addEventListener('push', (event) => {
  console.log('[SW] Push event received:', event);

  if (!event.data) {
    console.warn('[SW] Push event has no data');
    return;
  }

  let payload;
  try {
    payload = event.data.json();
  } catch (e) {
    console.error('[SW] Failed to parse push data:', e);
    payload = {
      title: 'Todo Reminder',
      body: event.data.text(),
    };
  }

  const options = {
    body: payload.body || 'You have a task reminder',
    icon: payload.icon || '/icon-192x192.png',
    badge: payload.badge || '/badge-72x72.png',
    tag: payload.tag || 'todo-notification',
    requireInteraction: payload.requireInteraction !== false,
    data: payload.data || {},
    actions: [
      {
        action: 'view',
        title: 'View Task',
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
      },
    ],
  };

  event.waitUntil(
    self.registration.showNotification(payload.title || 'Todo App', options)
  );
});

/**
 * Handle notification click events
 *
 * Opens the app when the user clicks on a notification
 */
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event);

  event.notification.close();

  if (event.action === 'dismiss') {
    return;
  }

  // Get the URL to open from the notification data
  const urlToOpen = event.notification.data?.url || '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Check if there's already a window open
        for (const client of clientList) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            // Navigate existing window to the URL and focus it
            client.navigate(urlToOpen);
            return client.focus();
          }
        }
        // No window open, open a new one
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

/**
 * Handle notification close events
 *
 * Logs when notifications are dismissed
 */
self.addEventListener('notificationclose', (event) => {
  console.log('[SW] Notification closed:', event.notification.tag);
});

/**
 * Service Worker install event
 *
 * Called when a new service worker is being installed
 */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker v' + SW_VERSION);
  // Skip waiting to activate immediately
  self.skipWaiting();
});

/**
 * Service Worker activate event
 *
 * Called when the service worker becomes active
 */
self.addEventListener('activate', (event) => {
  console.log('[SW] Service worker activated v' + SW_VERSION);
  // Claim all clients immediately
  event.waitUntil(clients.claim());
});
