def calculate_api(antecedent_rain_3d: float, decay_factor: float = 0.9) -> float:
    """Antecedent Precipitation Index - measure of soil saturation from past rainfall.
    API = sum(P_i * K^i) where K is decay factor (0.85-0.98)
    Higher API = more saturated soil = higher flood risk"""
    # Simulate 3-day API with exponential decay
    api = antecedent_rain_3d * decay_factor  # Simplified for single value input
    return round(api, 2)

def adjust_cn_for_moisture(cn_base: float, soil_moisture: float) -> float:
    """Adjust Curve Number based on Antecedent Moisture Condition (AMC).
    AMC I (dry): soil_moisture < 30% -> CN decreases
    AMC II (normal): 30-60% -> CN unchanged
    AMC III (wet): > 60% -> CN increases
    Formula from SCS Engineering Handbook"""
    if soil_moisture < 30:
        cn_adj = (4.2 * cn_base) / (10 - 0.058 * cn_base)  # AMC I
    elif soil_moisture > 60:
        cn_adj = (23 * cn_base) / (10 + 0.13 * cn_base)  # AMC III
    else:
        cn_adj = cn_base  # AMC II
    return round(min(cn_adj, 99), 2)

def calculate_potential_retention(cn: float) -> float:
    """S = (25400 / CN) - 254 (in mm)
    S is the maximum potential retention after runoff begins"""
    if cn <= 0:
        return 999.0
    s = (25400 / cn) - 254
    return round(max(s, 0), 2)

def calculate_scs_runoff(rainfall_mm: float, cn: float) -> float:
    """SCS Curve Number method for direct runoff.
    Q = (P - 0.2*S)^2 / (P + 0.8*S)
    where P = rainfall, S = potential retention
    Returns Q in mm"""
    s = calculate_potential_retention(cn)
    ia = 0.2 * s  # Initial abstraction
    if rainfall_mm <= ia:
        return 0.0
    q = ((rainfall_mm - ia) ** 2) / (rainfall_mm + 0.8 * s)
    return round(q, 2)

def calculate_time_concentration(slope: float, elevation: float) -> float:
    """Kirpich formula for time of concentration.
    Tc = 0.0195 * L^0.77 * S^(-0.385)
    where L = channel length (estimated from elevation), S = slope
    Returns Tc in minutes"""
    import math
    slope_fraction = max(slope / 100, 0.001)  # Convert degrees to fraction, avoid zero
    length_m = elevation * 0.5  # Rough estimate of channel length from elevation
    length_m = max(length_m, 100)  # Minimum 100m
    tc = 0.0195 * (length_m ** 0.77) * (slope_fraction ** (-0.385))
    return round(min(tc, 360), 2)  # Cap at 6 hours

def engineer_all_features(rainfall_6h: float, rainfall_24h: float, soil_moisture: float,
                          slope: float, elevation: float, cn: float,
                          antecedent_rain: float) -> dict:
    """Master function: compute ALL derived features from 7 raw inputs.
    Returns dict with raw + engineered features."""
    api_value = calculate_api(antecedent_rain)
    cn_adjusted = adjust_cn_for_moisture(cn, soil_moisture)
    potential_retention = calculate_potential_retention(cn_adjusted)
    runoff = calculate_scs_runoff(rainfall_6h, cn_adjusted)
    time_conc = calculate_time_concentration(slope, elevation)
    
    return {
        'raw': {
            'rainfall_6h': rainfall_6h,
            'rainfall_24h': rainfall_24h,
            'soil_moisture': soil_moisture,
            'slope': slope,
            'elevation': elevation,
            'cn': cn,
            'antecedent_rain': antecedent_rain
        },
        'engineered': {
            'api': api_value,
            'cn_adjusted': cn_adjusted,
            'potential_retention_mm': potential_retention,
            'expected_runoff_mm': runoff,
            'time_concentration_min': time_conc
        }
    }
