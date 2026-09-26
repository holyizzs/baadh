import time
import random
import requests

API_URL = "http://localhost:8000/api/predict"

SENSORS = [
    {"id": "NODE_01", "location": "Rudraprayag", "base": {"rainfall_6h": 10, "rainfall_24h": 15, "soil_moisture": 45, "slope": 25, "elevation": 1200, "cn": 75, "antecedent_rain": 10}},
    {"id": "NODE_02", "location": "Chamoli", "base": {"rainfall_6h": 5, "rainfall_24h": 10, "soil_moisture": 50, "slope": 30, "elevation": 1500, "cn": 70, "antecedent_rain": 5}},
    {"id": "NODE_03", "location": "Kedarnath", "base": {"rainfall_6h": 20, "rainfall_24h": 30, "soil_moisture": 60, "slope": 40, "elevation": 3583, "cn": 80, "antecedent_rain": 40}},
    {"id": "NODE_04", "location": "Uttarkashi", "base": {"rainfall_6h": 8, "rainfall_24h": 12, "soil_moisture": 40, "slope": 20, "elevation": 1150, "cn": 65, "antecedent_rain": 8}},
    {"id": "NODE_05", "location": "Pithoragarh", "base": {"rainfall_6h": 15, "rainfall_24h": 20, "soil_moisture": 55, "slope": 35, "elevation": 1600, "cn": 72, "antecedent_rain": 25}},
]

def simulate_sensors() -> None:
    """Continuously simulate sensor data every 10 seconds."""
    print("Starting IoT Sensor Simulation... Press Ctrl+C to stop.")
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n--- Batch {iteration} ---")
        
        for sensor in SENSORS:
            # Gradually increase features to simulate escalating rainfall
            sensor['base']['rainfall_6h'] += random.uniform(0.5, 5.0)
            sensor['base']['rainfall_24h'] += random.uniform(1.0, 7.0)
            sensor['base']['soil_moisture'] = min(100.0, sensor['base']['soil_moisture'] + random.uniform(0.5, 2.0))
            sensor['base']['antecedent_rain'] += random.uniform(0.1, 2.0)
            
            data = sensor['base']
            
            try:
                response = requests.post(API_URL, json=data, timeout=3)
                if response.status_code == 200:
                    result = response.json()
                    pred = result.get('prediction', result)
                    prob = pred.get('flood_probability', 0) * 100
                    risk = pred.get('risk_level', 'UNKNOWN')
                    print(f"[{sensor['id']} - {sensor['location']}] Risk: {risk} | Prob: {prob:.1f}% | Rain_6h: {data['rainfall_6h']:.1f}mm | Soil: {data['soil_moisture']:.1f}%")
                else:
                    print(f"[{sensor['id']}] Error: {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"[{sensor['id']}] Backend offline. Could not send data: {data}")
                
        time.sleep(10)

if __name__ == "__main__":
    try:
        simulate_sensors()
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
