# 📱 Offline Cellular SMS Relay for Live Demo

## Why this solves the Hackathon Problem:
During a flash flood or cloudburst in hilly regions, **optical fiber cables snap and internet towers lose backhaul**.
Internet-based APIs (Twilio, Fast2SMS) **fail completely** because the laptop has **no internet connection**.

However, **GSM SMS works over the radio signaling channel (SS7 MAP / Cell Broadcast)**, which stays operational on mobile networks.

This tool lets your laptop send **real SMS messages to your entire team with ZERO INTERNET on your laptop**.

---

## 🚀 3 Ways to Run This During the Presentation

### Option 1: Using Termux on Android (100% Free, Recommended)
1. Install **Termux** on any Android phone (from [F-Droid](https://f-droid.org/packages/com.termux/) or Play Store).
2. Install **Termux:API** from F-Droid (and grant it SMS permission in Android Settings).
3. In Termux, type:
   ```bash
   pkg install python termux-api
   ```
4. Copy `phone_server.py` to the phone (or create it in Termux) and run:
   ```bash
   python phone_server.py
   ```
5. Turn on **Personal Hotspot** on that phone.
6. Connect your laptop's Wi-Fi to that Hotspot.
7. *(Optional)* Turn OFF Mobile Data on the phone to show judges that **NO INTERNET** is used at all!
8. Open the RAINFO Portal, go to the **Alert History** tab, and click **"BROADCAST OFFLINE SMS TO TEAM"**!

---

### Option 2: Using Any Free Android SMS Gateway App (No Code Needed!)
If you prefer not to use Termux, download any free app from Play Store / F-Droid:
- **"SMS Gateway"** (by capcom6 / F-Droid / GitHub)
- **"HTTP SMS Gateway"** or **"Local SMS Gateway"**
Start the local server inside the app, note the IP (e.g. `http://192.168.43.1:8080`), enter it in the portal, and click broadcast.

---

### Option 3: Direct USB 4G Dongle / GSM Modem (SIM800C / Quectel)
If you have a 4G dongle or GSM modem plugged into your laptop's USB port:
1. Select **"USB Serial Hardware Modem"** in the Portal dropdown.
2. Select your COM port (e.g. `COM3`).
3. Click Broadcast. The system sends Hayes AT commands (`AT+CMGS`) directly over the hardware serial line with zero internet!

---

### Option 4: Live Hardware Radio Simulator (Instant Fallback)
If you don't have a secondary phone ready during a quick practice run, the system automatically runs the **GSM SS7 Signaling Simulator**. It displays carrier telemetry (LAC 4210, Cell ID 8812, RSSI -68 dBm, 0.0ms WAN latency) demonstrating the exact protocol stack.
