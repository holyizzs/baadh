"""
Firebase Cloud Messaging (FCM) push notification service.
Delivers flood alerts to the mobile PWA (/mobile) and makes the phone BEEP.

How it works:
1. Mobile devices open /mobile, enable notifications, and POST their FCM token
   to /api/alerts/register-device -> stored in devices.json (same pattern as team_directory.json).
2. dispatch_alert() calls send_push_alert() for every registered device whose
   subscribed district matches (or 'ALL').
3. FCM v1 API is used with a service-account OAuth token. When Firebase
   credentials are not configured the service degrades gracefully: the push
   channel reports 'not_configured' and everything else keeps working.

Setup (one time, free):
1. Firebase Console -> Project settings -> Service accounts -> "Generate new
   private key" -> save as backend/firebase-service-account.json
2. Get the web app's firebaseConfig object (Project settings -> General ->
   Your apps -> Web app) and paste it into mobile/firebase-config.js
"""

import os
import json
import time
import logging
import threading
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# ponytail: JSON file token store, not a DB — fine for demo scale (<10k devices).
# Upgrade path: swap load/save for a Postgres table, rest of the file unchanged.
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "push_devices.json"))
import app.config as _config
SA_FILE = _config.settings.FIREBASE_SERVICE_ACCOUNT_PATH

FCM_SCOPE = "https://www.googleapis.com/auth/firebase.messaging"
FCM_SEND_URL = "https://fcm.googleapis.com/v1/{project}/messages:send"

# Android notification channel used by the PWA service worker.
CRITICAL_CHANNEL_ID = "flood_alerts_critical"

_file_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Device token registry
# ---------------------------------------------------------------------------

def _load_devices() -> List[Dict[str, Any]]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading push device registry: {e}")
    return []


def _save_devices(devices: List[Dict[str, Any]]) -> bool:
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving push device registry: {e}")
        return False


def register_device(token: str, district: str = "ALL", label: str = "") -> Dict[str, Any]:
    """Register or update a device's FCM token and subscribed district."""
    token = (token or "").strip()
    district = (district or "ALL").strip()
    if not token:
        return {"success": False, "error": "Missing FCM token"}

    with _file_lock:
        devices = _load_devices()
        for d in devices:
            if d.get("token") == token:
                d["district"] = district
                if label:
                    d["label"] = label
                d["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                _save_devices(devices)
                return {"success": True, "updated": True, "devices": len(devices)}
        devices.append({
            "token": token,
            "district": district,
            "label": label,
            "registered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        _save_devices(devices)
    return {"success": True, "updated": False, "devices": len(devices)}


def unregister_device(token: str) -> Dict[str, Any]:
    with _file_lock:
        devices = _load_devices()
        remaining = [d for d in devices if d.get("token") != token]
        removed = len(remaining) < len(devices)
        if removed:
            _save_devices(remaining)
    return {"success": True, "removed": removed}


def get_registered_devices() -> List[Dict[str, Any]]:
    """Devices for the status endpoint; tokens truncated for safety."""
    return [
        {
            "district": d.get("district", "ALL"),
            "label": d.get("label", ""),
            "registered_at": d.get("registered_at"),
            "token_preview": (d.get("token", "")[:12] + "…") if d.get("token") else "",
        }
        for d in _load_devices()
    ]


# ---------------------------------------------------------------------------
# Firebase credential handling
# ---------------------------------------------------------------------------

def _load_service_account() -> Optional[dict]:
    if not os.path.exists(SA_FILE):
        return None
    try:
        with open(SA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading Firebase service account: {e}")
        return None


def firebase_status() -> Dict[str, Any]:
    """Whether FCM sending is actually configured (has service account key)."""
    sa = _load_service_account()
    return {
        "configured": bool(sa and sa.get("project_id") and sa.get("private_key")),
        "project_id": (sa or {}).get("project_id"),
        "service_account_path": SA_FILE,
        "registered_devices": len(_load_devices()),
    }


# ponytail: mint one OAuth token and cache it until near expiry (SA keys valid 1h).
_cached_oauth: Dict[str, Any] = {"token": None, "expires_at": 0.0}


def _get_access_token(sa: dict) -> Optional[str]:
    if _cached_oauth["token"] and time.time() < _cached_oauth["expires_at"] - 60:
        return _cached_oauth["token"]
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleAuthRequest

        creds = service_account.Credentials.from_service_account_info(
            sa, scopes=[FCM_SCOPE]
        )
        creds.refresh(GoogleAuthRequest())
        _cached_oauth["token"] = creds.token
        _cached_oauth["expires_at"] = time.time() + 3600
        return creds.token
    except ImportError:
        logger.error("google-auth not installed — run: pip install google-auth")
        return None
    except Exception as e:
        logger.error(f"FCM OAuth failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Sending
# ---------------------------------------------------------------------------

def _build_push_payload(district: str, risk_level: str, probability: float,
                        lead_time_hrs: float) -> Dict[str, Any]:
    """FCM v1 message body. Android channel + priority = device BEEPS loudly."""
    prob_pct = int(probability * 100) if probability <= 1.0 else int(probability)
    is_severe = risk_level.upper() in ("SEVERE", "CRITICAL")
    color = "#DC2626" if is_severe else "#F59E0B" if risk_level.upper() == "HIGH" else "#EAB308"
    title = f"🚨 {risk_level.upper()} FLOOD ALERT — {district}"
    body = (f"Flash flood probability {prob_pct}%. Lead time ~{lead_time_hrs}h. "
            f"Evacuate to high ground. Helpline 1078.")

    return {
        "message": {
            "notification": {"title": title, "body": body},
            "data": {
                "district": district,
                "risk_level": risk_level.upper(),
                "probability": str(prob_pct),
                "lead_time_hrs": str(lead_time_hrs),
                "beep": "true",
            },
            "android": {
                "priority": "HIGH",
                "notification": {
                    "channel_id": CRITICAL_CHANNEL_ID,
                    "color": color,
                    "default_sound": True,
                    "default_vibrate_timings": True,
                    "visibility": "PUBLIC",
                },
            },
            "webpush": {
                "notification": {
                    "title": title,
                    "body": body,
                    "icon": "/mobile/icons/icon-192.png",
                    "badge": "/mobile/icons/badge-72.png",
                    "tag": f"flood-{district}",
                    "renotify": True,
                    "requireInteraction": is_severe,
                },
                "fcm_options": {"link": "/mobile"},
            },
        }
    }


def _send_to_token(token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    sa = _load_service_account()
    if not (sa and sa.get("project_id") and sa.get("private_key")):
        return {"success": False, "status": "NOT_CONFIGURED",
                "error": "Firebase service account key missing (see push_service.py header)"}

    access = _get_access_token(sa)
    if not access:
        return {"success": False, "status": "AUTH_FAILED", "error": "Could not mint OAuth token"}

    import requests
    url = FCM_SEND_URL.format(project=sa["project_id"])
    body = dict(payload)
    body["message"]["token"] = token
    try:
        resp = requests.post(
            url, json=body,
            headers={"Authorization": f"Bearer {access}", "Content-Type": "application/json; UTF-8"},
            timeout=8,
        )
        if resp.status_code in (200, 201):
            return {"success": True, "status": "SENT", "message_id": resp.json().get("name", "")}
        # 404/410 = token is dead (app uninstalled); let caller prune it
        stale = resp.status_code in (404, 410)
        return {"success": False, "status": "STALE_TOKEN" if stale else "FCM_ERROR",
                "http": resp.status_code, "error": resp.text[:200]}
    except Exception as e:
        return {"success": False, "status": "NETWORK_ERROR", "error": str(e)}


def _targets_for(district: str, tokens: Optional[List[str]]) -> List[Dict[str, Any]]:
    if tokens is not None:
        return [{"token": t} for t in tokens]
    district_upper = (district or "ALL").upper()
    targets = []
    for d in _load_devices():
        if district_upper in ("ALL", "BROADCAST") or d.get("district", "ALL").upper() in (district_upper, "ALL"):
            targets.append({"token": d["token"]})
    return targets


def send_push_alert(district: str, risk_level: str, probability: float,
                    lead_time_hrs: float = 3.5,
                    tokens: Optional[List[str]] = None) -> Dict[str, Any]:
    """Push a flood alert to all registered devices for the district (or explicit tokens)."""
    status = firebase_status()
    targets = _targets_for(district, tokens)
    if not targets:
        return {"success": False, "status": "NO_DEVICES", "sent": 0, "failed": 0,
                "message": "No registered devices for this district. Open /mobile and enable alerts."}
    if not status["configured"]:
        return {"success": False, "status": "NOT_CONFIGURED", "sent": 0, "failed": len(targets),
                "message": status["service_account_path"]}

    payload = _build_push_payload(district, risk_level, probability, lead_time_hrs)
    sent, failed, stale = 0, 0, []
    for t in targets:
        res = _send_to_token(t["token"], payload)
        if res.get("success"):
            sent += 1
        else:
            failed += 1
            if res.get("status") == "STALE_TOKEN":
                stale.append(t["token"])

    if stale:
        with _file_lock:
            devices = _load_devices()
            _save_devices([d for d in devices if d.get("token") not in stale])
        logger.info(f"Pruned {len(stale)} stale FCM token(s)")

    return {
        "success": sent > 0,
        "status": "SENT" if sent else "ALL_FAILED",
        "sent": sent, "failed": failed, "pruned_stale": len(stale),
        "channel": "firebase_fcm",
    }
