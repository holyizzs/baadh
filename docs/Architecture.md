# System Architecture Document
# Flash Flood Prediction System

**Version:** 1.0  
**Date:** September 22, 2026  
**Last Updated:** September 22, 2026 5:44 PM IST  

---

## 1. SYSTEM OVERVIEW

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Web Dashboard  │  Mobile App  │  SMS  │  WhatsApp  │  Sirens  │
└────────┬──────────────┬─────────────────┬──────────────┬────────┘
         │              │                 │              │
┌────────▼──────────────▼─────────────────▼──────────────▼────────┐
│                    PRESENTATION LAYER                            │
├──────────────────────────────────────────────────────────────────┤
│         Frontend (HTML/CSS/JS)    │    Alert APIs                │
└────────┬─────────────────────────────────┬───────────────────────┘
         │                                 │
┌────────▼─────────────────────────────────▼───────────────────────┐
│                     APPLICATION LAYER                             │
├───────────────────────────────────────────────────────────────────┤
│  FastAPI Backend  │  ML Inference  │  Alert Manager  │  Scheduler│
└────────┬──────────────┬──────────────────┬──────────────┬─────────┘
         │              │                  │              │
┌────────▼──────────────▼──────────────────▼──────────────▼─────────┐
│                       DATA LAYER                                   │
├────────────────────────────────────────────────────────────────────┤
│  PostgreSQL/SQLite  │  Model Files (.pkl)  │  Static Data (DEM)   │
└────────┬──────────────────────────────────────────────┬───────────┘
         │                                              │
┌────────▼──────────────────────────────────────────────▼───────────┐
│                    EXTERNAL INTEGRATIONS                           │
├────────────────────────────────────────────────────────────────────┤
│  IoT Sensors  │  IMD API  │  SMS Gateway  │  Firebase  │  WhatsApp│
└────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
1. DATA COLLECTION
   IoT Sensors → ESP32 → LoRa Gateway → Backend API
   IMD API → Scheduled Job → Backend Storage
   User Input → Frontend Form → Backend API

2. PREDICTION
   Raw Data → Feature Engineering → ML Model → Prediction Result

3. ALERT GENERATION
   Prediction (Risk ≥ 70%) → Alert Manager → Multi-Channel Delivery
   
4. VISUALIZATION
   Backend API → Frontend Dashboard → User's Browser
```

---

## 2. TECHNOLOGY STACK

### 2.1 Frontend Stack

```yaml
Framework: Vanilla JavaScript (ES6+)
Styling: Tailwind CSS v3.3+ (CDN)
Charts: Chart.js v4.4+ (CDN)
Maps: Leaflet.js v1.9+ (CDN) OR Mapbox GL JS v2.15+
HTTP Client: Fetch API (native)
Build Tool: None (single HTML file for demo)

Browser Support:
  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+
```

**File Structure:**
```
frontend/
├── index.html              # Main dashboard (COMPLETE ✅)
├── assets/
│   ├── logo.png           # Project logo
│   └── india-flag.png     # For theme
└── README.md              # Setup instructions
```

### 2.2 Backend Stack

```yaml
Framework: FastAPI v0.104+
Language: Python 3.10+
ASGI Server: Uvicorn v0.24+
ML Library: Scikit-learn v1.3+ (Random Forest)
Data Processing: Pandas v2.1+, NumPy v1.24+
Model Persistence: Joblib v1.3+
HTTP Client: Requests v2.31+
Environment: python-dotenv v1.0+

Optional (Production):
  Database: PostgreSQL v15+ with TimescaleDB
  Cache: Redis v7+
  Task Queue: Celery v5+
```

**File Structure:**
```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry
│   ├── config.py                  # Configuration settings
│   ├── models/
│   │   ├── predictor.py          # ML model inference
│   │   └── feature_engineering.py # Physics calculations
│   ├── api/
│   │   ├── predict.py            # Prediction endpoints
│   │   ├── sensors.py            # Sensor data endpoints
│   │   └── alerts.py             # Alert endpoints
│   ├── services/
│   │   ├── alert_service.py      # Alert delivery logic
│   │   └── sms_service.py        # SMS gateway integration
│   └── utils/
│       ├── validation.py         # Input validation
│       └── logger.py             # Logging utilities
├── ml_models/
│   ├── flood_model.pkl           # Trained model
│   └── scaler.pkl                # Feature scaler
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container config
└── .env.example                  # Environment variables template
```

### 2.3 Machine Learning Stack

```yaml
Training:
  - Framework: Scikit-learn
  - Model: Random Forest Classifier (100 trees)
  - Alternative: LSTM-GRU (TensorFlow/Keras) if time permits
  
Feature Engineering:
  - Raw features: 7 (rainfall, soil, slope, elevation, etc.)
  - Calculated features: 5 (API, CN_adj, S, Q, Tc)
  - Total input: 12 features
  
Data:
  - Format: CSV
  - Size: 220-1000 rows
  - Split: 80% train, 20% test
  - Validation: K-fold cross-validation (k=5)
```

**File Structure:**
```
ml/
├── data/
│   ├── raw/
│   │   └── dataset.csv           # User-collected data
│   ├── processed/
│   │   └── features.csv          # Engineered features
│   └── external/
│       └── dem/                  # Terrain data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── scripts/
│   ├── feature_engineering.py    # Reusable module
│   ├── train_model.py           # Training script
│   └── evaluate_model.py        # Evaluation script
└── models/
    ├── flood_model.pkl          # Saved model
    └── scaler.pkl               # Saved scaler
```

### 2.4 IoT Stack (Optional for Demo)

```yaml
Microcontroller: ESP32 DevKit
Sensors:
  - Rain Gauge: Tipping bucket sensor
  - Soil Moisture: Capacitive sensor
  - Water Level: Ultrasonic (HC-SR04)
  - Weather: DHT22 (temp/humidity)
  
Communication: LoRaWAN or 4G/WiFi
Power: Solar panel (5W) + LiPo battery (12V 7Ah)
Programming: Arduino IDE (C++)
Gateway: Raspberry Pi 4 (Python)

Protocol:
  - Sensor → ESP32: I2C / Digital GPIO
  - ESP32 → Gateway: LoRa (868 MHz) or MQTT over WiFi
  - Gateway → Backend: HTTPS REST API
```

**File Structure:**
```
iot/
├── esp32_sensor_node/
│   ├── esp32_sensor_node.ino    # Arduino code
│   ├── config.h                 # WiFi/LoRa credentials
│   └── README.md                # Hardware setup
├── gateway/
│   ├── lora_receiver.py         # LoRa gateway
│   ├── mqtt_forwarder.py        # MQTT to API
│   └── requirements.txt
└── simulation/
    └── sensor_simulator.py      # Fake sensor data for demo
```

### 2.5 Alert Delivery Stack

```yaml
SMS:
  - Provider: MSG91 or Fast2SMS
  - API: REST
  - Cost: ₹0.20-0.50 per SMS
  
WhatsApp:
  - Method: WhatsApp Business API (via Gupshup) OR Manual groups
  - Cost: Free for groups, ₹0.30+ for API
  
Push Notifications:
  - Provider: Firebase Cloud Messaging (FCM)
  - Cost: Free
  - Platform: Android + iOS
  
Voice Calls (IVRS):
  - Provider: Exotel or Knowlarity
  - Cost: ₹0.50-1.00 per minute
  
Social Media:
  - Twitter API v2
  - Cost: Free (standard tier)
```

---

## 3. API SPECIFICATIONS

### 3.1 Core Endpoints

#### POST /api/predict
**Purpose:** Generate flood prediction for given conditions

**Request:**
```json
{
  "rainfall_6h": 85.0,
  "rainfall_24h": 130.0,
  "soil_moisture": 75.0,
  "slope": 32.0,
  "elevation": 2100.0,
  "cn": 74.0,
  "antecedent_rain": 95.0,
  "location": {
    "village": "Rudraprayag",
    "lat": 30.2850,
    "lon": 78.9900
  }
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "flood_probability": 0.87,
    "risk_level": "SEVERE",
    "risk_color": "#EF4444",
    "prediction": "FLOOD",
    "confidence": 0.82,
    "features": {
      "cn_adjusted": 90.2,
      "potential_retention_mm": 27.6,
      "expected_runoff_mm": 59.0,
      "time_concentration_min": 14.0,
      "api": 75.5
    },
    "threshold": {
      "runoff_threshold_mm": 45.0,
      "exceeded_by_percent": 31.1
    },
    "timing": {
      "time_to_flood_hours": 3.5,
      "expected_at": "2026-09-22T21:15:00Z"
    },
    "actions": [
      "Evacuate immediately to higher ground",
      "Move to Village B (3km north)",
      "Alert issued to authorities",
      "Secure livestock and essential belongings"
    ]
  },
  "timestamp": "2026-09-22T17:44:52Z"
}
```

#### GET /api/sensors/latest
**Purpose:** Get latest readings from all sensors

**Response:**
```json
{
  "success": true,
  "sensors": [
    {
      "id": "SENSOR_001",
      "name": "Rudraprayag Station",
      "location": {
        "village": "Rudraprayag",
        "lat": 30.2850,
        "lon": 78.9900
      },
      "status": "online",
      "last_reading": {
        "timestamp": "2026-09-22T17:40:00Z",
        "rainfall_mm": 15.2,
        "rainfall_6h": 85.0,
        "soil_moisture_pct": 75.0,
        "water_level_cm": 45.0,
        "temperature_c": 22.5,
        "humidity_pct": 78.0
      },
      "battery_percent": 87,
      "signal_strength": -65
    }
  ],
  "total_sensors": 5,
  "online_sensors": 4,
  "offline_sensors": 1,
  "timestamp": "2026-09-22T17:44:52Z"
}
```

#### POST /api/alerts/send
**Purpose:** Manually trigger alert for a village

**Request:**
```json
{
  "village": "Rudraprayag",
  "risk_level": "SEVERE",
  "probability": 0.87,
  "channels": ["sms", "whatsapp", "push", "siren"],
  "message": "Custom alert message (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "alert_id": "ALERT_20260922_174452_001",
  "village": "Rudraprayag",
  "delivery": {
    "sms": {
      "sent": 250,
      "failed": 3,
      "cost_inr": 62.50
    },
    "whatsapp": {
      "sent": 180,
      "failed": 0
    },
    "push": {
      "sent": 120,
      "failed": 5
    },
    "siren": {
      "activated": true,
      "pattern": "emergency"
    }
  },
  "timestamp": "2026-09-22T17:44:52Z"
}
```

#### GET /api/alerts/history
**Purpose:** Get alert history for analysis

**Query Parameters:**
- `village` (optional): Filter by village
- `risk_level` (optional): Filter by risk level
- `start_date` (optional): Start date (ISO format)
- `end_date` (optional): End date (ISO format)
- `limit` (optional): Number of results (default 50)

**Response:**
```json
{
  "success": true,
  "alerts": [
    {
      "id": "ALERT_20260922_174452_001",
      "village": "Rudraprayag",
      "risk_level": "SEVERE",
      "probability": 0.87,
      "issued_at": "2026-09-22T17:44:52Z",
      "acknowledged": true,
      "actual_flood": null,
      "false_alarm": null
    }
  ],
  "total": 125,
  "page": 1,
  "pages": 3
}
```

#### GET /api/health
**Purpose:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 3600,
  "model_loaded": true,
  "database_connected": true,
  "timestamp": "2026-09-22T17:44:52Z"
}
```

---

## 4. DATABASE SCHEMA

### 4.1 Tables (PostgreSQL / SQLite)

#### sensors
```sql
CREATE TABLE sensors (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    village VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    status VARCHAR(20) DEFAULT 'online',
    installed_date DATE,
    last_maintenance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### sensor_readings
```sql
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) REFERENCES sensors(id),
    timestamp TIMESTAMP NOT NULL,
    rainfall_mm DECIMAL(6, 2),
    rainfall_6h DECIMAL(6, 2),
    soil_moisture_pct DECIMAL(5, 2),
    water_level_cm DECIMAL(6, 2),
    temperature_c DECIMAL(5, 2),
    humidity_pct DECIMAL(5, 2),
    battery_percent INTEGER,
    signal_strength INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sensor_time (sensor_id, timestamp)
);
```

#### predictions
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    village VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    timestamp TIMESTAMP NOT NULL,
    flood_probability DECIMAL(5, 4) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    expected_runoff_mm DECIMAL(6, 2),
    time_to_flood_hours DECIMAL(5, 2),
    input_features JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_village_time (village, timestamp),
    INDEX idx_risk_level (risk_level, timestamp)
);
```

#### alerts
```sql
CREATE TABLE alerts (
    id VARCHAR(100) PRIMARY KEY,
    village VARCHAR(100) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    probability DECIMAL(5, 4) NOT NULL,
    message TEXT,
    issued_at TIMESTAMP NOT NULL,
    channels_used TEXT[], -- ['sms', 'whatsapp', 'push']
    delivery_stats JSONB,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_at TIMESTAMP,
    actual_flood BOOLEAN,
    false_alarm BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_village_issued (village, issued_at),
    INDEX idx_risk_level (risk_level, issued_at)
);
```

#### flood_events
```sql
CREATE TABLE flood_events (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    village VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    severity VARCHAR(20),
    casualties INTEGER DEFAULT 0,
    damage_estimate_inr BIGINT,
    description TEXT,
    rainfall_6h DECIMAL(6, 2),
    rainfall_24h DECIMAL(6, 2),
    soil_moisture DECIMAL(5, 2),
    slope DECIMAL(5, 2),
    elevation DECIMAL(7, 2),
    cn DECIMAL(5, 2),
    antecedent_rain DECIMAL(6, 2),
    source VARCHAR(50), -- 'manual', 'news', 'official'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_date (date),
    INDEX idx_village (village)
);
```

### 4.2 Simplified Schema for Demo (SQLite)

For hackathon demo, use in-memory SQLite or skip database entirely:

```python
# Option 1: In-memory dictionary
predictions_cache = {}
sensor_data_cache = {}
alert_history = []

# Option 2: SQLite in-memory
import sqlite3
conn = sqlite3.connect(':memory:')
```

---

## 5. DEPLOYMENT ARCHITECTURE

### 5.1 Development (Hackathon Demo)

```
Local Machine:
├── Backend: http://localhost:8000 (Uvicorn)
├── Frontend: file:///path/to/index.html (Browser)
├── Model: Loaded in memory from .pkl files
└── Database: In-memory or SQLite (optional)

No Docker, no cloud deployment needed for demo.
```

### 5.2 Production (Post-Hackathon)

```
┌─────────────────────────────────────────────────────┐
│                  LOAD BALANCER                      │
│            (AWS ALB / Nginx / Caddy)                │
└──────────┬──────────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │  Frontend   │
    │  (Vercel/   │
    │   Netlify)  │
    └─────────────┘
           │
    ┌──────▼────────────────────────────┐
    │     Backend API Cluster           │
    │  (AWS EC2 / Docker Swarm / K8s)   │
    │  ├── API Server 1                 │
    │  ├── API Server 2                 │
    │  └── API Server 3                 │
    └──────┬────────────────────────────┘
           │
    ┌──────▼──────────────────┐
    │     PostgreSQL          │
    │  (AWS RDS / DigitalOcean)│
    └─────────────────────────┘
           │
    ┌──────▼──────────────────┐
    │     Redis Cache         │
    │  (AWS ElastiCache)      │
    └─────────────────────────┘
```

---

## 6. SECURITY ARCHITECTURE

### 6.1 API Security

**For Demo:**
- No authentication (public access)
- Rate limiting: 100 req/min per IP
- Input validation (prevent injection)
- CORS enabled for frontend domain

**For Production:**
- JWT authentication for authenticated endpoints
- API keys for integrations
- Rate limiting: 1000 req/min per user
- HTTPS only (TLS 1.3)
- Input validation + sanitization
- SQL injection prevention (parameterized queries)
- XSS prevention (output escaping)

### 6.2 Data Security

- Passwords hashed with bcrypt (if auth implemented)
- API keys stored in environment variables (never in code)
- Database credentials in .env file (not committed)
- Sensitive data encrypted at rest (production)
- Audit logs for all alert sends

---

## 7. MONITORING & LOGGING

### 7.1 Application Logging

```python
# Logging levels
DEBUG: Feature calculations, model inputs
INFO: API requests, predictions made, alerts sent
WARNING: High prediction latency, sensor offline
ERROR: Model load failure, SMS delivery failed
CRITICAL: Database connection lost, system down
```

### 7.2 Metrics to Track

**Performance:**
- Prediction response time (p50, p95, p99)
- API endpoint latency
- Model inference time
- Alert delivery time

**Business:**
- Predictions per day
- Alerts sent per day
- Alert delivery success rate
- False alarm rate
- Missed flood rate (if actual flood occurred)

**Infrastructure:**
- CPU usage
- Memory usage
- Disk usage
- Network traffic

---

## 8. SCALABILITY CONSIDERATIONS

### 8.1 Horizontal Scaling

**Stateless API:** All API servers are identical, no sticky sessions needed

**Load Distribution:**
```
User requests → Load Balancer → Any API server
                               → Shared database
                               → Shared cache
```

**Auto-scaling rules:**
- Scale up: If CPU > 70% for 5 minutes, add server
- Scale down: If CPU < 30% for 10 minutes, remove server

### 8.2 Database Scaling

**Read Replicas:** For analytics queries, sensor data reads

**Partitioning:** Partition `sensor_readings` by date (monthly partitions)

**Archival:** Move old data (>1 year) to cold storage (S3)

---

## 9. DISASTER RECOVERY

### 9.1 Backup Strategy

**Database:**
- Automated daily backups
- Point-in-time recovery (last 30 days)
- Backup retention: 90 days

**Model Files:**
- Version controlled in Git
- Stored in S3 with versioning
- Model registry for production models

### 9.2 Failover Plan

**If primary backend fails:**
1. Load balancer detects failure (health check)
2. Routes traffic to secondary backend
3. Alert DevOps team
4. Primary restored within 1 hour

**If database fails:**
1. Promote read replica to primary (if available)
2. Fall back to cached predictions (Redis)
3. Restore from backup (RTO: 4 hours max)

---

## 10. INTEGRATION POINTS

### 10.1 External APIs

```
IMD Weather API:
  - Endpoint: https://mausam.imd.gov.in/api
  - Auth: API key (if available) or web scraping
  - Rate limit: Unknown, implement caching
  
MSG91 SMS API:
  - Endpoint: https://api.msg91.com
  - Auth: API key in header
  - Rate limit: 100 SMS/second
  
Firebase FCM:
  - Endpoint: https://fcm.googleapis.com
  - Auth: Server key
  - Rate limit: Unlimited (free)
  
WhatsApp Business API:
  - Via BSP (Gupshup/Kaleyra)
  - Auth: API key
  - Rate limit: BSP-dependent
```

### 10.2 Data Sources

```
Terrain Data:
  - Source: SRTM (earthexplorer.usgs.gov)
  - Format: GeoTIFF (30m resolution)
  - Size: ~500 MB for Uttarakhand
  - Update frequency: Static
  
Land Use Data:
  - Source: ISRO Bhuvan
  - Format: Shapefile
  - Update frequency: Annual
  
Historical Floods:
  - Source: User collection + NDMA reports
  - Format: CSV
  - Update frequency: Continuous
```

---

## 11. FILE & FOLDER STRUCTURE

### 11.1 Complete Project Structure

```
flash-flood-prediction/
├── frontend/
│   ├── index.html                 # Dashboard (✅ COMPLETE)
│   ├── assets/
│   │   └── logo.png
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app
│   │   ├── config.py             # Settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── predictor.py      # ML inference
│   │   │   └── feature_engineering.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py
│   │   │   ├── sensors.py
│   │   │   └── alerts.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── alert_service.py
│   │   │   └── sms_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validation.py
│   │       └── logger.py
│   ├── ml_models/
│   │   ├── flood_model.pkl
│   │   └── scaler.pkl
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── ml/
│   ├── data/
│   │   ├── raw/
│   │   │   └── dataset.csv
│   │   ├── processed/
│   │   │   └── features.csv
│   │   └── external/
│   │       └── dem/
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   └── 03_model_training.ipynb
│   ├── scripts/
│   │   ├── feature_engineering.py
│   │   ├── train_model.py
│   │   └── evaluate_model.py
│   └── models/
│       ├── flood_model.pkl
│       └── scaler.pkl
│
├── iot/ (optional)
│   ├── esp32_sensor_node/
│   │   └── esp32_sensor_node.ino
│   ├── gateway/
│   │   └── lora_receiver.py
│   └── simulation/
│       └── sensor_simulator.py
│
├── demo/
│   ├── kedarnath_demo.py
│   └── sensor_simulator.py
│
├── docs/
│   ├── PRD.md                    # ✅ COMPLETE
│   ├── Architecture.md           # ✅ THIS FILE
│   ├── Rules.md                  # TODO
│   ├── Phases.md                 # TODO
│   ├── Design.md                 # TODO
│   ├── Memory.md                 # TODO (created during coding)
│   └── PROJECT_CONTEXT.md        # ✅ COMPLETE
│
├── tests/
│   ├── test_api.py
│   ├── test_prediction.py
│   └── test_alerts.py
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## 12. TECHNOLOGY DECISIONS RATIONALE

### 12.1 Why FastAPI?
- ✅ Fast (async support)
- ✅ Auto-generated API docs (Swagger)
- ✅ Type hints for validation
- ✅ Easy to learn
- ✅ Modern Python framework

### 12.2 Why Random Forest over LSTM?
- ✅ Faster training (<3 minutes vs 20+ minutes)
- ✅ Works with small datasets (200+ samples)
- ✅ No GPU required
- ✅ Interpretable (feature importance)
- ✅ Good accuracy (80-85%)
- ⚠️ LSTM is better but needs more data + time

### 12.3 Why Vanilla JS over React?
- ✅ Zero build process (faster development)
- ✅ Single HTML file (easier to demo)
- ✅ No npm dependencies
- ✅ Faster page load
- ⚠️ React is better for production but overkill for demo

### 12.4 Why PostgreSQL over MongoDB?
- ✅ Better for time-series data (TimescaleDB extension)
- ✅ ACID compliance (critical for alerts)
- ✅ Strong geospatial support (PostGIS)
- ✅ Free and open source
- ⚠️ SQLite for demo (simpler)

---

## 13. PERFORMANCE BENCHMARKS

### 13.1 Target Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| API Prediction | <500ms | User expects instant result |
| Dashboard Load | <3s | Acceptable for web app |
| Alert Delivery | <5 min | Critical for emergency |
| Model Training | <5 min | Fast iteration during dev |
| Concurrent Users | 1000+ | District-level deployment |

### 13.2 Optimization Strategies

**Backend:**
- Cache predictions (Redis) for 30 seconds
- Load model once at startup (not per request)
- Use connection pooling for database
- Async I/O for external APIs

**Frontend:**
- Lazy load charts (Chart.js)
- Debounce user input (prediction form)
- Compress images (logo, assets)
- Minify JS/CSS (production only)

**Database:**
- Index frequently queried columns (timestamp, village)
- Partition large tables (sensor_readings by date)
- Use materialized views for analytics

---

## 14. APPENDIX

### 14.1 Environment Variables

```bash
# Backend (.env file)
APP_ENV=development  # development | production
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000

# Database (optional for demo)
DATABASE_URL=sqlite:///./flood.db
# DATABASE_URL=postgresql://user:pass@localhost:5432/flood_db

# Model
MODEL_PATH=./ml_models/flood_model.pkl
SCALER_PATH=./ml_models/scaler.pkl

# Alert Services
MSG91_API_KEY=your_msg91_key
MSG91_SENDER_ID=FLDALT
FIREBASE_SERVER_KEY=your_firebase_key
WHATSAPP_API_KEY=your_whatsapp_key

# External APIs
IMD_API_KEY=your_imd_key  # if available

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:8000

# Monitoring (optional)
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
```

### 14.2 Dependencies

**Backend (requirements.txt):**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pandas==2.1.3
numpy==1.24.4
scikit-learn==1.3.2
joblib==1.3.2
requests==2.31.0
python-multipart==0.0.6

# Optional for production
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
sqlalchemy==2.0.23
```

**Frontend:** Zero dependencies (all CDN)

**ML (for training):**
```txt
pandas==2.1.3
numpy==1.24.4
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
jupyter==1.0.0
notebook==7.0.6
```

---

**END OF ARCHITECTURE DOCUMENT**

*Next: See Rules.md for AI coding guidelines*  
*See Phases.md for development roadmap*  
*See Design.md for visual design system*
