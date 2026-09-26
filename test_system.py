#!/usr/bin/env python3
"""
Ponytail Assert-Based Verification Self-Check.
Zero frameworks, zero fixtures, runs in < 1 second.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.models.feature_engineering import (
    calculate_api,
    adjust_cn_for_moisture,
    calculate_scs_runoff,
    calculate_time_concentration,
    engineer_all_features
)
from app.models.predictor import FloodPredictor


def run_checks():
    print("Running Ponytail Verification Self-Check...")

    # 1. Physics Calibrations
    assert calculate_api(50.0) == 45.0, "API calculation failed"
    assert adjust_cn_for_moisture(75.0, 80.0) > 75.0, "AMC III CN adjustment failed"
    assert calculate_scs_runoff(10.0, 70.0) == 0.0, "Runoff below abstraction must be 0"
    assert calculate_scs_runoff(150.0, 85.0) > 80.0, "Runoff calculation error"
    assert calculate_time_concentration(35.0, 3000.0) > 0, "Time of concentration must be positive"
    print("  [PASS] Hydrological physics calculations verified.")

    # 2. Predictor & Hybrid ML Model
    predictor = FloodPredictor()
    assert predictor.model_loaded, "Predictor model must be loaded"

    # Test Low Risk
    f_low = engineer_all_features(8, 14, 25, 18, 1200, 65, 5)
    res_low = predictor.predict(f_low)
    assert res_low['risk_level'] == 'LOW', f"Expected LOW risk, got {res_low['risk_level']}"
    assert res_low['flood_probability'] < 0.35, "Low risk prob must be < 0.35"
    print(f"  [PASS] Low condition: {res_low['flood_probability']*100:.1f}% -> LOW")

    # Test High/Severe Risk (Kedarnath Peak)
    f_high = engineer_all_features(340, 420, 99, 35, 3583, 74, 340)
    res_high = predictor.predict(f_high)
    assert res_high['risk_level'] == 'SEVERE', f"Expected SEVERE risk, got {res_high['risk_level']}"
    assert res_high['flood_probability'] > 0.85, "Severe risk prob must be > 0.85"
    print(f"  [PASS] Extreme condition: {res_high['flood_probability']*100:.1f}% -> SEVERE")

    print("\nAll 3 core invariants held. System verified.")


if __name__ == "__main__":
    run_checks()
