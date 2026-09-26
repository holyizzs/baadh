# RAINFO — Flash Flood Early Warning System (FFEWS)

An intelligent, physics-informed AI Flash Flood Early Warning System engineered for high-altitude mountainous terrains (Himalayan regions, Northeast India, and Western Ghats). Built for disaster management authorities (NDMA/SDMA) and citizens.

---

## 📌 Key Capabilities

- **Hybrid Physics-Informed ML Engine**: Combines calibrated hydrological equations (SCS-CN runoff, Antecedent Precipitation Index, Kirpich time-of-concentration) with a trained Random Forest model.
- **NDMA/IMD 4-Tier Hazard Alert Scale**: Classifies risk into `LOW` (Green), `MODERATE` (Yellow), `HIGH` (Orange), and `SEVERE` (Red Emergency).
- **NDMA Officer Console (`/officer`)**: Operational dashboard with live Leaflet topography, flood probability gauges, and emergency alert broadcast controls.
- **Citizen Public Portal (`/user`)**: Mobile-friendly public portal with district risk heatmaps, flood safety guidelines, and emergency helpline directories.
- **Offline SMS Relay (`/android_relay`)**: Field-deployable, zero-dependency offline SMS relay that broadcasts SMS alerts via local phone hotspot even if cellular internet towers collapse.
- **Mobile Alert PWA (`/mobile`)**: Progressive Web App with Firebase Cloud Messaging (FCM) push alerts and siren beeps.
- **Interactive Simulations**: Replays historical disaster timelines (e.g. Kedarnath 2013) and simulates live IoT river/rain gauge telemetry.

---

## 📂 Repository Structure

```text
├── backend/                  # FastAPI Core Engine & Services
│   ├── app/
│   │   ├── api/              # REST Endpoints (alerts, predict, rainfall, sensors)
│   │   ├── models/           # Hydrological physics, feature engineering & predictor
│   │   ├── services/         # SMS (Fast2SMS), FCM Push, POC Directory, Offline Relay
│   │   ├── utils/            # Logging and schema validations
│   │   ├── config.py         # App configurations
│   │   └── main.py           # FastAPI entrypoint & static route mounting
│   ├── requirements.txt      # Python backend dependencies
│   └── .env.example          # Environment variable template
├── mobile/                   # Progressive Web App (PWA) for mobile alerts
│   ├── index.html            # Citizen alert receiver UI
│   ├── fcm-sw.js             # Service Worker for push notifications & alarm audio
│   ├── manifest.json         # PWA Manifest
│   └── icons/                # PWA App icons
├── android_relay/            # Offline SMS Android Termux Server
│   ├── phone_server.py       # Standalone HTTP server for offline SMS forwarding
│   └── README.md             # Android hotspot & Termux setup instructions
├── ml/                       # Machine Learning Training Pipeline
│   ├── scripts/train_model.py# Model training & cross-validation script
│   ├── data/                 # Raw and engineered feature datasets
│   └── model_report.json     # Accuracy, Precision, Recall, and ROC-AUC metrics
├── ml_models/                # Exported model weights (.pkl) and evaluation metrics
├── demo/                     # Demonstration & Simulation Scripts
│   ├── kedarnath_demo.py     # Step-by-step Kedarnath 2013 disaster scenario replay
│   └── sensor_simulator.py   # IoT sensor stream simulator
├── docs/                     # Specifications & Research Documentation
│   ├── Architecture.md       # Full System Architecture
│   ├── Design.md             # Detailed Technical Design
│   └── PRD.md                # Product Requirements Document
├── portal.html               # Gateway Landing Page (Citizen / Officer selection)
├── index.html                # NDMA Officer Operational Console
├── user.html                 # Citizen Early Warning Portal
├── districts.html            # Monitored Districts & Evacuation Shelter Directory
├── dataset.csv               # Calibrated hydrological dataset
├── India_Flood_Incidents_Data.csv # Historical flood benchmarks
├── test_system.py            # Physics & model assertion self-check test suite
├── test_push.py              # Push notification assertion test suite
├── start_system.bat          # Windows one-click launcher
└── .gitignore                # Clean GitHub ignore rules
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `backend/.env` and update required keys (optional for local testing):
```bash
cp backend/.env.example backend/.env
```

### 4. Run Verification Self-Checks
Verify hydrological calculations, ML predictors, and push notification services:
```bash
python test_system.py
python test_push.py
```

### 5. Launch Application
**Windows One-Click:**
Double click `start_system.bat` or run:
```bash
start_system.bat
```

**Manual Launch:**
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 Web Endpoints

Once running, access the portals in your browser:

| Portal | URL | Description |
| :--- | :--- | :--- |
| **Gateway** | `http://localhost:8000/` | Entry portal to select Citizen or Officer mode |
| **Public Citizen Portal** | `http://localhost:8000/user` | Real-time threat tiers, safety guidelines, and maps |
| **NDMA Officer Console** | `http://localhost:8000/officer` | Command center for monitoring and broadcasting alerts |
| **Districts Directory** | `http://localhost:8000/districts`| Monitored districts & shelter directory |
| **Mobile Alert PWA** | `http://localhost:8000/mobile` | Citizen alert subscriber app |
| **Interactive API Docs**| `http://localhost:8000/docs` | OpenAPI / Swagger interactive documentation |

---

## 🧪 Demos & Testing

### Replay Kedarnath 2013 Flash Flood Event
Simulate the timeline of the Kedarnath disaster to verify early warning trigger thresholds:
```bash
python demo/kedarnath_demo.py
```

### Simulate Real-time IoT Sensors
Stream live rainfall and soil moisture readings into the API:
```bash
python demo/sensor_simulator.py
```

---

## 📄 License
This project was developed for disaster risk reduction and early warning applications.
