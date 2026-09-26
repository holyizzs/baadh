def validate_rainfall(value: float) -> float:
    """Validate rainfall input (0-500mm)."""
    if not (0.0 <= value <= 500.0):
        raise ValueError(f"Rainfall value {value} is out of bounds (0-500mm).")
    return float(value)

def validate_soil_moisture(value: float) -> float:
    """Validate soil moisture input (0-100%)."""
    if not (0.0 <= value <= 100.0):
        raise ValueError(f"Soil moisture value {value} is out of bounds (0-100%).")
    return float(value)

def validate_slope(value: float) -> float:
    """Validate slope input (0-90 degrees)."""
    if not (0.0 <= value <= 90.0):
        raise ValueError(f"Slope value {value} is out of bounds (0-90 degrees).")
    return float(value)

def validate_elevation(value: float) -> float:
    """Validate elevation input (0-9000m)."""
    if not (0.0 <= value <= 9000.0):
        raise ValueError(f"Elevation value {value} is out of bounds (0-9000m).")
    return float(value)

def validate_curve_number(value: float) -> float:
    """Validate curve number input (0-100)."""
    if not (0.0 <= value <= 100.0):
        raise ValueError(f"Curve number value {value} is out of bounds (0-100).")
    return float(value)
