#!/usr/bin/env python3
"""
Push notification self-check (same style as test_system.py).
Zero frameworks, runs in < 1 second, no network or Firebase keys needed.
"""

import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.services import push_service


def run_checks():
    print("Running push service self-check...")

    # Isolate the registry in a temp dir so we never touch real device data
    with tempfile.TemporaryDirectory() as tmp:
        push_service.DATA_FILE = os.path.join(tmp, "push_devices.json")

        # 1. Registration: insert, update, dedupe
        r1 = push_service.register_device("tok-aaa-111", "Rudraprayag", "Phone A")
        assert r1["success"] and not r1["updated"] and r1["devices"] == 1, "first registration failed"
        r2 = push_service.register_device("tok-bbb-222", "ALL", "Phone B")
        r3 = push_service.register_device("tok-aaa-111", "Chamoli", "Phone A moved")
        assert r3["updated"] and r3["devices"] == 2, "re-registration must update, not duplicate"
        with open(push_service.DATA_FILE, encoding="utf-8") as f:
            stored = {d["token"]: d for d in json.load(f)}
        assert stored["tok-aaa-111"]["district"] == "Chamoli", "district update not persisted"
        print("  [PASS] Device registration persists and updates without duplicates.")

        # 2. District targeting: subscriber matches own district; ALL matches everything
        t_rp = push_service._targets_for("Rudraprayag", None)
        assert [t["token"] for t in t_rp] == ["tok-bbb-222"], "ALL-subscriber must receive Rudraprayag alert"
        t_k = push_service._targets_for("Kedarnath", None)
        assert [t["token"] for t in t_k] == ["tok-bbb-222"], "district alert must reach ALL-subscribers only"
        t_bcast = push_service._targets_for("BROADCAST", None)
        assert len(t_bcast) == 2, "BROADCAST must reach every device"
        t_explicit = push_service._targets_for("Chamoli", ["tok-aaa-111"])
        assert [t["token"] for t in t_explicit] == ["tok-aaa-111"], "explicit token list must pass through"
        print("  [PASS] District targeting (own district / ALL / broadcast / explicit tokens).")

        # 3. Payload structure: Android critical channel + beep flag for loud alerts
        payload = push_service._build_push_payload("Rudraprayag", "SEVERE", 0.87, 7.5)
        msg = payload["message"]
        assert msg["android"]["notification"]["channel_id"] == push_service.CRITICAL_CHANNEL_ID
        assert msg["android"]["priority"] == "HIGH"
        assert msg["data"]["beep"] == "true"
        assert msg["data"]["probability"] == "87"
        assert "87" in msg["notification"]["body"] or "87" in msg["webpush"]["notification"]["body"]
        assert msg["webpush"]["notification"]["requireInteraction"] is True
        mild = push_service._build_push_payload("Rudraprayag", "MODERATE", 0.4, 3.5)
        assert mild["message"]["webpush"]["notification"]["requireInteraction"] is False
        print("  [PASS] FCM payload: HIGH priority, critical channel, beep data, severity gating.")

        # 4. Graceful degradation: no Firebase key -> clean NOT_CONFIGURED, no crash
        assert push_service.firebase_status()["configured"] is False, "must report unconfigured without SA key"
        res = push_service.send_push_alert("BROADCAST", "SEVERE", 0.9)
        assert res["status"] == "NOT_CONFIGURED" and res["failed"] == 2 and res["sent"] == 0, \
            f"expected graceful NOT_CONFIGURED, got {res}"
        print("  [PASS] Without Firebase key: alerts degrade to NOT_CONFIGURED (system keeps running).")

        # 5. Unregistration
        push_service.unregister_device("tok-aaa-111")
        assert len(push_service.get_registered_devices()) == 1, "unregister must remove the device"
        print("  [PASS] Device unregistration.")

    print("\nAll 5 push invariants held. Push service verified.")


if __name__ == "__main__":
    run_checks()
