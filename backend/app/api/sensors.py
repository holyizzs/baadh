import random
from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()

SENSORS = [
    {'id': 'SENSOR_001', 'name': 'Kedarnath Station', 'village': 'Kedarnath', 'lat': 30.7346, 'lon': 79.0669, 'status': 'online'},
    {'id': 'SENSOR_002', 'name': 'Rudraprayag Station', 'village': 'Rudraprayag', 'lat': 30.2849, 'lon': 78.9816, 'status': 'online'},
    {'id': 'SENSOR_003', 'name': 'Chamoli Station', 'village': 'Chamoli', 'lat': 30.4025, 'lon': 79.3240, 'status': 'online'},
    {'id': 'SENSOR_004', 'name': 'Uttarkashi Station', 'village': 'Uttarkashi', 'lat': 30.7268, 'lon': 78.4354, 'status': 'online'},
    {'id': 'SENSOR_005', 'name': 'Pithoragarh Station', 'village': 'Pithoragarh', 'lat': 29.5826, 'lon': 80.2183, 'status': 'offline'},
]

@router.get('/sensors/latest')
async def get_latest_sensors() -> dict:
    """Return sensors with simulated live readings."""
    random.seed(42)  # For reproducible demo, though could be omitted in real dynamic mock
    sensors_with_readings = []
    for sensor in SENSORS:
        reading = {
            **sensor,
            'last_reading': {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'rainfall_mm': round(random.uniform(0, 30), 1),
                'rainfall_6h': round(random.uniform(10, 120), 1),
                'soil_moisture_pct': round(random.uniform(40, 90), 1),
                'water_level_cm': round(random.uniform(10, 80), 1),
                'temperature_c': round(random.uniform(15, 28), 1),
                'humidity_pct': round(random.uniform(60, 95), 1),
            },
            'battery_percent': random.randint(50, 100),
            'signal_strength': random.randint(-90, -40)
        }
        sensors_with_readings.append(reading)
    
    online = sum(1 for s in SENSORS if s['status'] == 'online')
    return {
        'success': True,
        'sensors': sensors_with_readings,
        'total_sensors': len(SENSORS),
        'online_sensors': online,
        'offline_sensors': len(SENSORS) - online,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
