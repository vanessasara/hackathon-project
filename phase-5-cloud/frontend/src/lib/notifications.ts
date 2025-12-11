/**
 * Browser Push Notification utilities
 *
 * Part B: Advanced Features - Push Notifications
 *
 * This module handles:
 * - Service Worker registration
 * - Push notification permission requests
 * - Push subscription management
 */

/**
 * VAPID public key from environment
 * This must match the private key on the server
 */
const VAPID_PUBLIC_KEY = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY || '';

/**
 * Result type for notification initialization
 * Provides detailed error information for user feedback
 */
export interface NotificationResult {
  success: boolean;
  error?: string;
  step?: 'support' | 'permission' | 'service-worker' | 'subscription' | 'backend';
}

/**
 * Check if push notifications are supported
 */
export function isPushSupported(): boolean {
  return (
    'serviceWorker' in navigator &&
    'PushManager' in window &&
    'Notification' in window
  );
}

/**
 * Get current notification permission status
 */
export function getNotificationPermission(): NotificationPermission {
  if (!('Notification' in window)) {
    return 'denied';
  }
  return Notification.permission;
}

/**
 * Request notification permission from the user
 *
 * @returns Promise resolving to the permission status
 */
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!('Notification' in window)) {
    console.warn('[Notifications] Notifications not supported');
    return 'denied';
  }

  if (Notification.permission === 'granted') {
    return 'granted';
  }

  if (Notification.permission === 'denied') {
    console.warn('[Notifications] Notifications were previously denied');
    return 'denied';
  }

  // Request permission
  const permission = await Notification.requestPermission();
  return permission;
}

/**
 * Register the service worker
 *
 * @returns Promise resolving to the ServiceWorkerRegistration
 */
export async function registerServiceWorker(): Promise<ServiceWorkerRegistration | null> {
  if (!('serviceWorker' in navigator)) {
    console.warn('[Notifications] Service Workers not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
    });
    console.log('[Notifications] Service Worker registered:', registration.scope);
    return registration;
  } catch (error) {
    console.error('[Notifications] Service Worker registration failed:', error);
    return null;
  }
}

/**
 * Create a fresh push subscription
 * Always unsubscribes existing subscription first to ensure we get a fresh one
 *
 * @param registration - The service worker registration
 * @returns Promise resolving to the PushSubscription
 */
export async function subscribeToPush(
  registration: ServiceWorkerRegistration
): Promise<PushSubscription | null> {
  const vapidKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY || VAPID_PUBLIC_KEY;

  if (!vapidKey || vapidKey.length === 0) {
    console.error('[Notifications] VAPID public key not configured');
    return null;
  }

  try {
    // ALWAYS unsubscribe existing subscription first
    // This ensures we create a fresh subscription that gets sent to backend
    const existing = await registration.pushManager.getSubscription();
    if (existing) {
      console.log('[Notifications] Unsubscribing existing push subscription');
      await existing.unsubscribe();
    }

    // Create new subscription with VAPID key
    console.log('[Notifications] Creating new push subscription...');
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(vapidKey),
    });

    console.log('[Notifications] Created new push subscription');
    return subscription;
  } catch (error) {
    console.error('[Notifications] Failed to subscribe to push:', error);
    return null;
  }
}

/**
 * Unsubscribe from push notifications
 *
 * @param registration - The service worker registration
 */
export async function unsubscribeFromPush(
  registration: ServiceWorkerRegistration
): Promise<boolean> {
  try {
    const subscription = await registration.pushManager.getSubscription();

    if (subscription) {
      await subscription.unsubscribe();
      console.log('[Notifications] Unsubscribed from push notifications');
      return true;
    }

    return false;
  } catch (error) {
    console.error('[Notifications] Failed to unsubscribe from push:', error);
    return false;
  }
}

/**
 * Send push subscription to the backend
 *
 * @param subscription - The PushSubscription to send
 * @param authToken - JWT auth token
 */
export async function sendSubscriptionToBackend(
  subscription: PushSubscription,
  authToken: string
): Promise<{ success: boolean; error?: string }> {
  const subscriptionJson = subscription.toJSON();

  if (!subscriptionJson.endpoint || !subscriptionJson.keys) {
    console.error('[Notifications] Invalid subscription data');
    return { success: false, error: 'Invalid subscription data' };
  }

  console.log('[Notifications] Sending subscription to backend...');
  console.log('[Notifications] Endpoint:', subscriptionJson.endpoint.substring(0, 50) + '...');

  try {
    const response = await fetch('/api/push-subscriptions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        endpoint: subscriptionJson.endpoint,
        p256dh_key: subscriptionJson.keys.p256dh,
        auth_key: subscriptionJson.keys.auth,
        user_agent: navigator.userAgent,
      }),
    });

    if (response.ok) {
      console.log('[Notifications] Push subscription saved to backend successfully');
      return { success: true };
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      console.error('[Notifications] Failed to save push subscription:', response.status, errorText);

      if (response.status === 401) {
        return { success: false, error: 'Authentication failed. Please log in again.' };
      } else if (response.status === 400) {
        return { success: false, error: 'Invalid subscription data' };
      } else {
        return { success: false, error: `Server error (${response.status})` };
      }
    }
  } catch (error) {
    console.error('[Notifications] Error saving push subscription:', error);
    return { success: false, error: 'Network error. Check your connection.' };
  }
}

/**
 * Remove push subscription from the backend
 *
 * @param endpoint - The subscription endpoint to remove
 * @param authToken - JWT auth token
 */
export async function removeSubscriptionFromBackend(
  endpoint: string,
  authToken: string
): Promise<boolean> {
  try {
    const response = await fetch('/api/push-subscriptions', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({ endpoint }),
    });

    if (response.ok || response.status === 204) {
      console.log('[Notifications] Push subscription removed from backend');
      return true;
    } else {
      console.error('[Notifications] Failed to remove push subscription:', response.status);
      return false;
    }
  } catch (error) {
    console.error('[Notifications] Error removing push subscription:', error);
    return false;
  }
}

/**
 * Initialize push notifications
 *
 * This is the main entry point for setting up push notifications.
 * Call this after the user logs in.
 *
 * @param authToken - JWT auth token
 * @returns Promise resolving to NotificationResult with detailed status
 */
export async function initializePushNotifications(
  authToken: string
): Promise<NotificationResult> {
  console.log('[Notifications] Starting push notification initialization...');

  // Check support
  if (!isPushSupported()) {
    console.warn('[Notifications] Push notifications not supported in this browser');
    return {
      success: false,
      error: 'Push notifications not supported in this browser',
      step: 'support'
    };
  }

  // Request permission
  console.log('[Notifications] Requesting permission...');
  const permission = await requestNotificationPermission();
  if (permission !== 'granted') {
    console.warn('[Notifications] Notification permission not granted:', permission);
    return {
      success: false,
      error: permission === 'denied'
        ? 'Notifications blocked. Please enable in browser settings.'
        : 'Notification permission not granted',
      step: 'permission'
    };
  }
  console.log('[Notifications] Permission granted');

  // Register service worker
  console.log('[Notifications] Registering service worker...');
  const registration = await registerServiceWorker();
  if (!registration) {
    return {
      success: false,
      error: 'Failed to register service worker',
      step: 'service-worker'
    };
  }

  // Wait for the service worker to be ready
  console.log('[Notifications] Waiting for service worker to be ready...');
  await navigator.serviceWorker.ready;
  console.log('[Notifications] Service worker ready');

  // Subscribe to push (always creates fresh subscription)
  console.log('[Notifications] Creating push subscription...');
  const subscription = await subscribeToPush(registration);
  if (!subscription) {
    return {
      success: false,
      error: 'Failed to create push subscription',
      step: 'subscription'
    };
  }

  // Send to backend
  console.log('[Notifications] Sending to backend...');
  const backendResult = await sendSubscriptionToBackend(subscription, authToken);
  if (!backendResult.success) {
    return {
      success: false,
      error: backendResult.error || 'Failed to save subscription',
      step: 'backend'
    };
  }

  console.log('[Notifications] Push notifications initialized successfully!');
  return { success: true };
}

/**
 * Convert a base64url string to an ArrayBuffer
 * Used for VAPID public key
 */
function urlBase64ToUint8Array(base64String: string): ArrayBuffer {
  try {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }

    return outputArray.buffer as ArrayBuffer;
  } catch (error) {
    console.error('[Notifications] Failed to decode VAPID key:', error);
    throw new Error('Invalid VAPID public key');
  }
}
