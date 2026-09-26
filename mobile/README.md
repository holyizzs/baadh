# 📱 RAINFO Mobile — Flood Alerts on Your Phone

A PWA (installable web app) that receives **Firebase Cloud Messaging (FCM) push
notifications** whenever the RAINFO backend dispatches a flood alert — and
**BEEPS loudly + vibrates** on the phone, even when the app is closed.

## Quick Start

### 1. Start the backend (serves the app)
```bash
start_system.bat          # or: cd backend && python -m uvicorn app.main:app --port 8000
```
The app is live at **http://localhost:8000/mobile** — open it on your phone
(same Wi-Fi, use the laptop's LAN IP like `http://192.168.x.x:8000/mobile`).

### 2. One-time Firebase setup (free)

**A. Service account key (backend → sends pushes):**
1. [Firebase Console](https://console.firebase.google.com) → your project
2. ⚙️ Project settings → **Service accounts** → **Generate new private key**
3. Save the downloaded JSON as `firebase-service-account.json` in the **project root**
   (next to `start_system.bat`)

**B. Web app config + VAPID key (phone → receives pushes):**
1. ⚙️ Project settings → **General** → Your apps → **Web app (`</>`)** → register it → copy the
   `firebaseConfig` object → paste into `mobile/firebase-config.js`
2. ⚙️ Project settings → **Cloud Messaging** → **Web Push certificates** → generate/copy the
   **Key pair** → paste as `vapidKey` in `mobile/firebase-config.js`

**C. Install the critical Android notification channel (one adb command, optional but recommended):**
```bash
adb shell cmd notification allow_listener com.rainline.floodalerts
```
*(Or simply enable the "Flood Alerts (critical)" channel in the app's Android notification settings after first alert.)*

### 3. On the phone
1. Open `http://<laptop-ip>:8000/mobile`
2. Pick your district → tap **🔔 Enable flood alerts & beep** → **Allow** notifications
3. Browser menu → **Install app / Add to Home screen**
4. Tap **📢 Test alert tone now** to hear the beep

That phone's token is now registered (`backend/app/data/push_devices.json`).

### 4. Fire a test alert
From the Officer Console (`/officer`) alert panel, or:
```bash
curl -X POST http://localhost:8000/api/alerts/send \
  -H "Content-Type: application/json" \
  -d '{"pin":"1078","village":"Rudraprayag","risk_level":"SEVERE","probability":0.9,"channels":["sms","push"]}'
```
→ every phone subscribed to `Rudraprayag` (or `ALL`) gets a push notification
with a **critical-priority beep + vibration** within seconds.

## How it works

```
Officer fires alert (portal / auto-predictor ≥70%)
        │
        ▼
backend alert_service.dispatch_alert(channels=[... 'push'])
        │
        ▼
push_service.send_push_alert()          ← device registry: push_devices.json
        │  FCM HTTP v1 + service-account OAuth (google-auth)
        ▼
Firebase Cloud Messaging  →  Google servers  →  phone (internet required)
        │
        ▼
mobile/fcm-sw.js (service worker, runs when app is closed)
   ├─ shows loud notification (vibrate pattern, renotify)
   └─ pings open app → WebAudio siren beep loop
```

- **Beep when closed:** the service worker's notification uses `vibrate` + the
  `flood_alerts_critical` Android channel (HIGH priority). When the app is
  open, an explicit WebAudio beep plays over the notification.
- **District targeting:** each device subscribes to one district or `ALL`;
  alerts match on district equality or `ALL`; `village="BROADCAST"` reaches everyone.
- **Graceful degradation:** no Firebase key / no devices / FCM error → the push
  channel reports a clean status in `delivery_stats.channels.push` and never
  crashes the alert pipeline (SMS/WhatsApp/siren are unaffected).
- **Stale tokens** (app uninstalled) are pruned automatically on 404/410 from FCM.

## New backend endpoints

| Endpoint | Purpose |
|---|---|
| `GET  /api/alerts/push/status` | Firebase config state + registered devices |
| `POST /api/alerts/register-device` | `{token, district, label}` from the PWA |
| `POST /api/alerts/unregister-device` | `{token}` — opt out |
| `POST /api/alerts/push/test` | `{token, district}` — send a sample SEVERE push to one device |

`dispatch_alert` gained a **`"push"` channel** (included in the API default).
The phone-facing side also exposes `/mobile` (PWA), `/mobile/manifest.json`,
`/mobile/fcm-sw.js` (FCM service worker).

## Files

| File | Role |
|---|---|
| `mobile/index.html` | The PWA — enable flow, district picker, beep engine, alert feed |
| `mobile/firebase-config.js` | **You paste your firebaseConfig + vapidKey here** |
| `mobile/fcm-sw.js` | Service worker: background push → loud notification → beep |
| `mobile/manifest.json` | Makes it installable (icon, theme, standalone) |
| `mobile/icons/` | Generated wave icons (`mobile/generate_icons.py` rebuilds them) |
| `backend/app/services/push_service.py` | FCM HTTP v1 sender, token registry, OAuth cache |
| `backend/app/data/push_devices.json` | Registered device tokens (created on first registration) |
| `test_push.py` | Self-check: registry, targeting, payload, graceful degradation — run with `backend\.venv\Scripts\python.exe test_push.py` |

## Notes & limits

- **Internet is required for push** (FCM relays via Google). Your offline SMS
  relay (`android_relay/`) covers the zero-internet demo path; push is the
  online path. Demo tip: show push first, then kill Wi-Fi and show the offline
  cellular broadcast — the two stories complement each other.
- Push works on **Chrome/Edge/Android and Safari 16.4+/iOS 16.4+** (iOS must be
  *installed to home screen* first). Demo on an Android phone for the loudest result.
- Tokens live in a JSON file — fine for demo scale; swap the load/save in
  `push_service.py` for a DB when you outgrow it (marked `ponytail:` in code).
- A venv was created at `backend/.venv` (Windows `py` launcher had no project
  deps). `requirements.txt` pins were nudged to Python-3.12-compatible versions
  (`numpy 1.26.4`, `pandas 2.1.4`, `scikit-learn 1.9.1` matching the trained
  model pickle) + `google-auth` for FCM auth.
