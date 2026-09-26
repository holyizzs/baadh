/**
 * RAINFO flood-alert service worker.
 * Runs even when the app is closed — this is what makes the phone BEEP at 3 AM.
 */

importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');
importScripts('./firebase-config.js');

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  const n = payload.notification || {};
  const d = payload.data || {};

  self.registration.showNotification(n.title || '🚨 Flood Alert', {
    body: n.body || 'Flash flood warning for your area.',
    icon: '/mobile/icons/icon-192.png',
    badge: '/mobile/icons/badge-72.png',
    tag: d.district ? 'flood-' + d.district : 'flood-alert',
    renotify: true,
    requireInteraction: (d.risk_level || '').toUpperCase().indexOf('SEVERE') !== -1,
    vibrate: [500, 150, 500, 150, 500, 150, 800],
    data: { link: '/mobile/' }
  });

  // Explicitly ring the device ringer for a loud, sustained beep
  if (d.beep === 'true') {
    self.registration.active && self.registration.active.postMessage({ type: 'BEEP_ALERT' });
  }
});

// Tapping the notification opens the app
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const link = (event.notification.data && event.notification.data.link) || '/mobile/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes('/mobile') && 'focus' in client) return client.focus();
      }
      return self.clients.openWindow(link);
    })
  );
});
