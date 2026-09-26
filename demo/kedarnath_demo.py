import time
import requests
import json

API_URL = "http://localhost:8000/api/predict"

TIMELINE_EVENTS = [
    {
        "time": "06:00 AM",
        "data": {"rainfall_6h": 40, "rainfall_24h": 40, "soil_moisture": 55, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 30},
        "note": "Morning rain starts."
    },
    {
        "time": "09:00 AM",
        "data": {"rainfall_6h": 75, "rainfall_24h": 90, "soil_moisture": 70, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 65},
        "note": "Rainfall intensifying."
    },
    {
        "time": "12:00 PM",
        "data": {"rainfall_6h": 120, "rainfall_24h": 160, "soil_moisture": 82, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 95},
        "note": "(HIGH ALERT ISSUED)"
    },
    {
        "time": "03:00 PM",
        "data": {"rainfall_6h": 240, "rainfall_24h": 290, "soil_moisture": 95, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 180},
        "note": "Continuous heavy downpour."
    },
    {
        "time": "05:00 PM",
        "data": {"rainfall_6h": 320, "rainfall_24h": 380, "soil_moisture": 98, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 280},
        "note": "Critical levels reached."
    },
    {
        "time": "07:30 PM",
        "data": {"rainfall_6h": 340, "rainfall_24h": 420, "soil_moisture": 99, "slope": 35, "elevation": 3583, "cn": 74, "antecedent_rain": 340},
        "note": "(FLOOD)"
    }
]

def print_colored(text: str, color: str = "white") -> None:
    """Print text in specified color to the console."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[0m",
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['white']}")

def run_kedarnath_demo() -> None:
    """Replay the Kedarnath 2013 timeline."""
    print_colored("--- RAINFO SYSTEM: KEDARNATH 2013 DISASTER REPLAY ---", "blue")
    
    for event in TIMELINE_EVENTS:
        print_colored(f"\n[{event['time']}] {event['note']}", "yellow")
        print(f"Features: {json.dumps(event['data'])}")
        
        try:
            response = requests.post(API_URL, json=event['data'], timeout=5)
            if response.status_code == 200:
                result = response.json()
                pred = result.get('prediction', result)
                prob = pred.get('flood_probability', 0)
                risk = pred.get('risk_level', 'UNKNOWN')
                actions = pred.get('actions', [])
                
                color = "green"
                if risk in ("HIGH", "SEVERE"): color = "red"
                elif risk == "MODERATE": color = "yellow"
                
                print_colored(f"Prediction: {prob*100:.2f}% Probability -> Risk: {risk}", color)
                if actions:
                    print_colored(f"  Actions: {', '.join(actions[:2])}", "white")
            else:
                print_colored(f"Error from API: {response.status_code} {response.text}", "red")
        except requests.exceptions.RequestException:
            print_colored("Backend not running. Ensure FastAPI is started on port 8000.", "red")
        
        if event["time"] == "12:00 PM":
            print_colored("\nALERT WOULD HAVE BEEN ISSUED AT 12:00 PM — 7.5 HOURS BEFORE DISASTER", "red")
            
        time.sleep(2)

if __name__ == "__main__":
    run_kedarnath_demo()
