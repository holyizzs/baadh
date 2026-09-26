# Product Requirements Document (PRD)
# Flash Flood Prediction System for Hilly Regions

**Version:** 1.0  
**Date:** September 22, 2026  
**Project Code:** SIH PS 26192  
**Owner:** Team FloodGuard AI  

---

## 1. EXECUTIVE SUMMARY

### 1.1 Problem Statement
Hilly states in India (Uttarakhand, Himachal Pradesh) face frequent flash floods with minimal warning time, resulting in significant loss of life and property. The 2013 Kedarnath disaster killed 5,700+ people with zero advance warning. Current systems provide only district-level warnings with 24+ hour delays, insufficient for flash floods that develop in 1-3 hours.

### 1.2 Solution Overview
A hyper-local flash flood early warning system that combines physics-based hydrological models with machine learning to predict floods at village-level (1-5 km²) with 3-6 hour advance warning time. The system integrates IoT sensors, real-time weather data, and terrain analysis to generate actionable alerts through multiple channels (SMS, WhatsApp, mobile app, sirens).

### 1.3 Success Metrics
- **Prediction Accuracy:** 80%+ on test data
- **Lead Time:** 3-6 hours for gradual-onset floods
- **Granularity:** Village-level (1-5 km² vs current 500+ km²)
- **False Alarm Rate:** <20%
- **Alert Delivery:** 95%+ reach within 5 minutes
- **Impact:** Potential to save 1000+ lives annually in Uttarakhand alone

---

## 2. TARGET USERS

### 2.1 Primary Users

**Profile 1: Village Residents**
- **Demographics:** Rural population in hilly regions, mixed literacy, age 15-70
- **Device Usage:** 60% smartphone, 95% basic mobile phone
- **Connectivity:** Intermittent 2G/3G, limited during heavy rains
- **Needs:**
  - Simple, clear alerts in local language (Hindi/regional)
  - Work offline or on low bandwidth
  - Audio/visual warnings (sirens, voice calls)
  - Actionable guidance (where to evacuate)

**Profile 2: Local Authorities**
- **Role:** Village Sarpanch, Block Development Officer, District Magistrate
- **Needs:**
  - Dashboard showing all villages under jurisdiction
  - Early alerts for resource mobilization
  - Historical data for planning
  - Export capabilities for reports

**Profile 3: Emergency Responders**
- **Role:** NDRF, State Disaster Response Force, Police, Fire Services
- **Needs:**
  - Real-time situational awareness
  - Predicted impact zones
  - Route planning for evacuations
  - Communication with field teams

### 2.2 Secondary Users

**Profile 4: Researchers/Planners**
- **Role:** Academic researchers, urban planners, NDMA officials
- **Needs:**
  - Historical flood data
  - Model performance metrics
  - API access for integrations
  - Bulk data export

**Profile 5: Tourists/Pilgrims**
- **Role:** Visitors to Char Dham, trekkers, adventure tourists
- **Needs:**
  - Real-time safety status
  - Multi-language support (English)
  - Easy-to-understand risk levels
  - Safe zone locations

---

## 3. CORE FEATURES & REQUIREMENTS

### 3.1 Must-Have Features (MVP)

#### F1: Real-Time Flood Prediction
**Description:** Predict flood probability at village level using hybrid physics-ML model  
**User Story:** As a village resident, I want to know the flood risk for my village in the next 6 hours so I can decide whether to evacuate  
**Acceptance Criteria:**
- System predicts flood probability (0-100%) for each monitored village
- Updates predictions every 30 minutes
- Shows risk level (LOW/MODERATE/HIGH/SEVERE) with color coding
- Displays expected time to flood if risk is elevated
- 80%+ accuracy on validation data

**Technical Requirements:**
- Input: 7 factors (rainfall, soil moisture, slope, elevation, drainage density, antecedent rain, curve number)
- Output: Flood probability, risk level, time to flood, expected runoff
- Model: Random Forest or LSTM-GRU ensemble
- Processing time: <500ms per prediction
- API endpoint: POST /api/predict

#### F2: Multi-Channel Alert System
**Description:** Deliver alerts via 6 channels to ensure 95%+ reach  
**User Story:** As a village resident, I want to receive flood alerts even if I don't have internet so I don't miss critical warnings  
**Acceptance Criteria:**
- SMS alerts sent via commercial gateway (MSG91/Fast2SMS)
- WhatsApp messages to village community groups
- Push notifications to mobile app users
- IoT sirens activated in village centers
- Voice calls (IVRS) for elderly/non-smartphone users
- Twitter/social media posts for awareness
- All alerts delivered within 5 minutes of risk detection

**Technical Requirements:**
- Alert priority: HIGH/SEVERE trigger all channels, MODERATE triggers SMS+WhatsApp+Push
- Message templates in Hindi + English
- Delivery status tracking
- Retry mechanism for failed deliveries
- Cost: <₹0.50 per alert per person

#### F3: Interactive Risk Dashboard
**Description:** Web-based dashboard showing real-time risk map and sensor data  
**User Story:** As a district official, I want to see all villages in my district on a map with color-coded risk levels so I can prioritize resources  
**Acceptance Criteria:**
- Map view with village boundaries color-coded by risk
- Click village to see detailed prediction
- Live sensor data table (rainfall, soil moisture, water level)
- Rainfall forecast chart (next 12 hours)
- Active alerts panel with timestamps
- Responsive design (works on desktop, tablet, mobile)

**Technical Requirements:**
- Built with HTML/CSS/JavaScript (Tailwind CSS)
- Map library: Leaflet.js or Mapbox
- Charts: Chart.js
- Updates every 30 seconds via polling
- Offline fallback for connectivity issues

#### F4: Manual Prediction Tool
**Description:** Allow users to input conditions and get instant prediction  
**User Story:** As a researcher, I want to test "what-if" scenarios by entering different rainfall amounts to understand flood thresholds  
**Acceptance Criteria:**
- Input form for 7 parameters
- Instant prediction on button click
- Display probability, risk level, expected runoff, time to flood
- Show recommended actions
- Comparison to historical threshold
- Export prediction as PDF/screenshot

**Technical Requirements:**
- Client-side validation of inputs
- Calls backend API /api/predict
- Shows loading state during calculation
- Error handling for invalid inputs

#### F5: Kedarnath 2013 Retrospective Demo
**Description:** Replay simulation showing how system would have performed during actual disaster  
**User Story:** As a judge/stakeholder, I want to see proof that this system would have saved lives during past disasters  
**Acceptance Criteria:**
- Hour-by-hour timeline from 6 AM to 7:30 PM (June 16, 2013)
- Show risk level progression
- Highlight when HIGH alert would have been issued (12:00 PM)
- Display lead time achieved (7.5 hours)
- Show potential lives saved calculation
- Dramatic presentation (animations, sound effects)

**Technical Requirements:**
- Modal/overlay interface
- Data: Historical rainfall and terrain for Kedarnath
- Animation: Risk meter climbing
- Timeline scrubber
- "Replay" button on dashboard

---

### 3.2 Should-Have Features (Post-MVP)

#### F6: Mobile Application (React Native)
**Description:** Native mobile app for offline alerts and location-based warnings  
**Priority:** HIGH  
**Timeline:** Phase 2 (Week 2-3)

#### F7: Evacuation Route Optimizer
**Description:** Calculate safest path to high ground based on real-time flood extent  
**Priority:** MEDIUM  
**Timeline:** Phase 3

#### F8: Historical Data Analytics
**Description:** Dashboard showing past floods, model performance trends, seasonal patterns  
**Priority:** MEDIUM  
**Timeline:** Phase 3

#### F9: Admin Panel
**Description:** User management, sensor management, alert history, configuration  
**Priority:** LOW  
**Timeline:** Phase 4

---

### 3.3 Won't-Have Features (Out of Scope)

❌ User authentication (not needed for public dashboard in demo)  
❌ Payment gateway (government-funded project)  
❌ Real-time drone footage integration  
❌ Predictive analytics for 7+ days (flash floods are <24 hour events)  
❌ Integration with dam release schedules (different data source, complex)  
❌ Multi-hazard prediction (landslides, earthquakes - separate models)  

---

## 4. USER FLOWS

### 4.1 Flow 1: Village Resident Receives Alert

```
1. System detects HIGH risk for Village A (87% probability)
2. Alert triggered across all channels
3. User receives SMS: "🚨 FLOOD ALERT - HIGH..."
4. User opens link → Dashboard shows Village A in orange
5. User sees: "Evacuate in 3 hours to Village B (3km north)"
6. User shares with family/neighbors
7. User evacuates to safe zone
8. System tracks acknowledgment (optional)
```

### 4.2 Flow 2: District Official Monitors Situation

```
1. Official opens dashboard on laptop
2. Sees 3 villages in orange (HIGH risk)
3. Clicks Village A → Detailed prediction popup
4. Notes: 87% probability, 3.5 hour lead time, 250 residents
5. Mobilizes NDRF team to Village A
6. Arranges buses for evacuation
7. Sets up relief camp in Village B
8. Monitors situation via dashboard real-time updates
```

### 4.3 Flow 3: Researcher Tests Prediction

```
1. Opens "Manual Prediction Tool" on dashboard
2. Enters: Rainfall=120mm, Soil=85%, Slope=38°, etc.
3. Clicks "PREDICT FLOOD RISK"
4. System shows: 95% SEVERE, Evacuate NOW
5. Researcher changes rainfall to 80mm
6. System shows: 65% MODERATE, Prepare to evacuate
7. Researcher identifies threshold: ~90mm rainfall = critical
8. Exports results for research paper
```

### 4.4 Flow 4: Judge Sees Kedarnath Demo

```
1. Judge opens dashboard during hackathon presentation
2. Team clicks "REPLAY DISASTER TIMELINE" button
3. Modal opens showing Kedarnath 2013 simulation
4. Timeline starts: 06:00 AM - LOW risk (40mm rain)
5. Progresses: 09:00 AM - MODERATE (75mm)
6. **12:00 PM - HIGH ALERT ISSUED** ⚠️
7. Continues: 03:00 PM - SEVERE (240mm)
8. Ends: 07:30 PM - FLOOD OCCURRED
9. Summary: "7.5 hour advance warning, 5000+ lives could be saved"
10. Judge is impressed, asks technical questions
```

---

## 5. TECHNICAL REQUIREMENTS

### 5.1 Performance Requirements

| Metric | Requirement | Rationale |
|--------|-------------|-----------|
| **Prediction Response Time** | <500ms | User expects instant results |
| **Dashboard Load Time** | <3 seconds | Acceptable for web dashboard |
| **Alert Delivery Time** | <5 minutes | Critical for emergency alerts |
| **System Uptime** | 99.5%+ | Downtime during monsoon = disaster |
| **Concurrent Users** | 1000+ | District officials + residents |
| **Data Refresh Rate** | 30 seconds | Balance between freshness and load |

### 5.2 Data Requirements

**Storage:**
- Historical flood events: ~500 records (5 MB)
- Sensor readings: 5 sensors × 6 readings/hour × 24 hours = 720 records/day (100 KB/day)
- Predictions: 50 villages × 48 predictions/day = 2,400 records/day (500 KB/day)
- Total: <10 MB/day → 3.6 GB/year

**Backup:**
- Daily automated backups
- 30-day retention for sensor data
- Permanent retention for flood events and predictions

### 5.3 Security Requirements

**For Demo (Hackathon):**
- No authentication required (public dashboard)
- API rate limiting: 100 requests/minute
- Input validation to prevent injection attacks

**For Production (Post-Hackathon):**
- Role-based access control (Admin, Official, Public)
- API key authentication for integrations
- HTTPS only
- Data encryption at rest
- Audit logs for critical actions

### 5.4 Scalability Requirements

**Phase 1 (Pilot):** 50 villages, 5 sensors, 10,000 residents  
**Phase 2 (District):** 500 villages, 50 sensors, 100,000 residents  
**Phase 3 (State):** 5,000 villages, 500 sensors, 1,000,000 residents  

Architecture must support 100x scale from Phase 1 to Phase 3.

---

## 6. CONSTRAINTS & ASSUMPTIONS

### 6.1 Constraints

**Technical:**
- No access to government Cell Broadcast System (CBS)
- IoT sensors have limited battery life (solar + battery, 30 days backup)
- Limited internet connectivity in remote areas (2G fallback)
- Budget: ₹10,000 for hardware in hackathon demo

**Timeline:**
- Hackathon: September 25, 2026 (3 days to build)
- MVP must work with limited historical data (50-100 flood events)

**Regulatory:**
- SMS/WhatsApp use commercial APIs (not government-integrated)
- Cannot issue "official" warnings (only advisory)
- Partnership with SDMA required for production deployment

### 6.2 Assumptions

**User Assumptions:**
- 95% of users have basic mobile phones (SMS capable)
- 60% have smartphones (WhatsApp + app capable)
- Village Sarpanch acts as information hub
- Communities conduct evacuation drills (not system's responsibility)

**Technical Assumptions:**
- IMD/NASA data remains freely available
- DEM terrain data is accurate (±10m elevation error acceptable)
- ML model can achieve 80%+ accuracy with 200+ training samples
- False alarms are acceptable (better safe than sorry)

**Environmental Assumptions:**
- Flash floods have 1-6 hour warning window (not <30 min cloudbursts)
- Soil moisture can be estimated from rainfall patterns if sensors unavailable
- Historical data from 2010-2024 is representative of future patterns

---

## 7. SUCCESS CRITERIA & KPIs

### 7.1 Hackathon Success (September 25, 2026)

✅ **Demo runs smoothly** - No crashes during 10-minute presentation  
✅ **Kedarnath replay impresses judges** - Emotional impact of "7.5 hour warning"  
✅ **Live prediction works** - Enter data, get instant result  
✅ **Questions answered confidently** - Team understands technical details  
✅ **Top 3 finish** - Win prize or recognition  

### 7.2 Pilot Deployment Success (6 months)

✅ **50 villages monitored** - Rudraprayag district  
✅ **80%+ prediction accuracy** - Validated on real events  
✅ **Zero casualties in predicted floods** - Successful evacuations  
✅ **Community acceptance** - Residents trust the system  
✅ **Partnership secured** - MoU with Uttarakhand SDMA  

### 7.3 Long-Term Success (2 years)

✅ **5,000 villages covered** - All Uttarakhand + Himachal Pradesh  
✅ **1,000+ lives saved** - Documented evacuations preventing deaths  
✅ **₹100 crore damage prevented** - Economic impact  
✅ **National recognition** - Adopted by NDMA as national model  
✅ **Expansion to other states** - J&K, Northeast, Western Ghats  

---

## 8. RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Insufficient training data** | Model accuracy <70% | HIGH | Use synthetic data + transfer learning from global datasets |
| **False alarms cause alert fatigue** | Users ignore future alerts | MEDIUM | Set high thresholds (70%+), explain uncertainty in messages |
| **Sensor failures during storm** | No real-time data | MEDIUM | Fallback to IMD satellite data, redundant sensors |
| **Internet connectivity loss** | Alerts not delivered | HIGH | SMS/IVRS don't need internet, local sirens work offline |
| **Government doesn't adopt** | No official integration | LOW | Focus on community adoption first, proven results attract govt |
| **Budget overrun** | Can't deploy hardware | MEDIUM | Start with simulation, add real sensors incrementally |

---

## 9. DEPENDENCIES

**External Dependencies:**
- IMD rainfall data API (or manual download)
- SRTM DEM data from USGS
- SMS gateway (MSG91/Fast2SMS) account
- WhatsApp Business API (or manual groups for demo)
- Firebase for push notifications
- Hosting (AWS/Azure free tier or local server for demo)

**Internal Dependencies:**
- Dataset collection (user's responsibility)
- ML model training (AI's responsibility)
- Frontend-backend integration
- Testing on real devices (mobile, tablet, desktop)

---

## 10. GLOSSARY

**API** - Antecedent Precipitation Index (measure of soil saturation from past rainfall)  
**CBS** - Cell Broadcast System (government emergency alert system)  
**CN** - Curve Number (SCS method parameter for land use)  
**DEM** - Digital Elevation Model (terrain height data)  
**FFG** - Flash Flood Guidance (rainfall threshold for flooding)  
**GLOF** - Glacial Lake Outburst Flood  
**IMD** - India Meteorological Department  
**IoT** - Internet of Things (sensors + connectivity)  
**IVRS** - Interactive Voice Response System (automated phone calls)  
**LSTM** - Long Short-Term Memory (type of neural network)  
**NDMA** - National Disaster Management Authority  
**NDRF** - National Disaster Response Force  
**SCS** - Soil Conservation Service (runoff calculation method)  
**SDMA** - State Disaster Management Authority  
**SMS** - Short Message Service (text messages)  

---

## 11. APPROVALS

**Prepared by:** Team FloodGuard AI  
**Reviewed by:** [Hackathon Mentor]  
**Approved by:** [Team Lead]  
**Date:** September 22, 2026  

**Next Review:** Post-Hackathon (September 26, 2026)  

---

**END OF PRD**

*For technical architecture, see Architecture.md*  
*For development phases, see Phases.md*  
*For visual design, see Design.md*
