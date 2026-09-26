import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

from app.models.predictor import FloodPredictor
from app.models.feature_engineering import engineer_all_features

logger = logging.getLogger(__name__)
router = APIRouter()
_predictor = FloodPredictor()

class PredictionInput(BaseModel):
    rainfall_6h: float = Field(..., ge=0, le=500, description='6-hour rainfall in mm')
    rainfall_24h: Optional[float] = Field(default=None, ge=0, le=1000, description='24-hour rainfall in mm')
    soil_moisture: float = Field(..., ge=0, le=100, description='Soil moisture percentage')
    slope: float = Field(..., ge=0, le=90, description='Slope in degrees')
    elevation: float = Field(..., ge=0, le=9000, description='Elevation in meters')
    cn: float = Field(..., ge=0, le=100, description='SCS Curve Number')
    antecedent_rain: float = Field(default=0, ge=0, le=500, description='3-day antecedent rainfall in mm')
    location: Optional[dict] = None

class PredictionResponse(BaseModel):
    success: bool
    prediction: dict
    timestamp: str

@router.post('/predict', response_model=PredictionResponse)
async def predict_flood(data: PredictionInput) -> PredictionResponse:
    """Generate flood prediction for given conditions."""
    try:
        rainfall_24h = data.rainfall_24h or (data.rainfall_6h * 2)
        
        features = engineer_all_features(
            rainfall_6h=data.rainfall_6h,
            rainfall_24h=rainfall_24h,
            soil_moisture=data.soil_moisture,
            slope=data.slope,
            elevation=data.elevation,
            cn=data.cn,
            antecedent_rain=data.antecedent_rain
        )
        
        result = _predictor.predict(features)
        
        return PredictionResponse(
            success=True,
            prediction=result,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    except ValueError as e:
        logger.error(f'Validation error during prediction: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f'Prediction failed: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Prediction failed: {str(e)}')
