/**
 * RAINFO Mobile — Firebase web app credentials.
 *
 * Paste YOUR firebaseConfig object here. Find it in:
 *   Firebase Console -> Project settings -> General -> Your apps -> Web app (</>)
 *
 * It must include a `vapidKey` for web push:
 *   Firebase Console -> Project settings -> Cloud Messaging -> Web Push certificates
 *   -> copy the key pair (create one if empty) and paste it below.
 *
 * Plain `var` on purpose: this file is loaded BOTH by the page (<script src>)
 * and by the service worker (importScripts), which don't share module scope.
 */
var firebaseConfig = {
  apiKey: "PASTE_YOUR_API_KEY",
  authDomain: "PASTE_YOUR_PROJECT.firebaseapp.com",
  projectId: "PASTE_YOUR_PROJECT_ID",
  storageBucket: "PASTE_YOUR_PROJECT.appspot.com",
  messagingSenderId: "PASTE_YOUR_SENDER_ID",
  appId: "PASTE_YOUR_APP_ID"
};

// Cloud Messaging -> Web Push certificates -> key pair
var vapidKey = "PASTE_YOUR_VAPID_PUBLIC_KEY";
