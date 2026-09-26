import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone

from app.api.predict import router as predict_router
from app.api.sensors import router as sensors_router
from app.api.alerts import router as alerts_router
from app.api.rainfall import router as rainfall_router
from app.models.predictor import FloodPredictor
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)

_start_time = time.time()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Flash Flood Early Warning System — NDMA Internal Portal"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api")
app.include_router(sensors_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(rainfall_router, prefix="/api")

# Mobile flood-alert PWA (receives Firebase push notifications and beeps)
import os as _os
from fastapi.staticfiles import StaticFiles
_mobile_dir = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", "mobile"))
if _os.path.isdir(_mobile_dir):
    app.mount("/mobile", StaticFiles(directory=_mobile_dir, html=True), name="mobile")


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize resources on startup."""
    logger.info("Initializing RAINFO application resources...")
    app.state.predictor = FloodPredictor()
    logger.info("FloodPredictor initialized successfully.")


from fastapi.responses import FileResponse, RedirectResponse
import os

@app.get("/")
def read_root():
    """Serve the RAINFO portal gateway (choose Public / Officer)."""
    gateway_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "portal.html"))
    if os.path.exists(gateway_path):
        return FileResponse(gateway_path)
    return RedirectResponse(url="/docs")


@app.get("/user")
def read_user_portal():
    """Serve the public RAINFO user portal."""
    user_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "user.html"))
    if os.path.exists(user_path):
        return FileResponse(user_path)
    return RedirectResponse(url="/")


@app.get("/officer")
def read_officer_console():
    """Serve the restricted NDMA operational console (index.html)."""
    officer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "index.html"))
    if os.path.exists(officer_path):
        return FileResponse(officer_path)
    return RedirectResponse(url="/")


@app.get("/portal.html")
def redirect_gateway_html():
    """Redirect gateway file URL to the gateway route."""
    return RedirectResponse(url="/", status_code=307)


@app.get("/user.html")
def redirect_user_portal_html():
    """Redirect legacy user.html URL to the public portal route."""
    return RedirectResponse(url="/user", status_code=307)


@app.get("/index.html")
def redirect_officer_html():
    """Redirect officer console file URL to the /officer route."""
    return RedirectResponse(url="/officer", status_code=307)


@app.get("/portal")
def redirect_old_admin_route():
    """Legacy admin route now points to the officer console."""
    return RedirectResponse(url="/officer", status_code=307)


@app.get("/admin")
def redirect_admin_route():
    """Admin route alias pointing to the officer console."""
    return RedirectResponse(url="/officer", status_code=307)


@app.get("/startup")
@app.get("/start_system")
def redirect_startup_route():
    """Direct route pointing to the System Architecture and Startup Guide."""
    return RedirectResponse(url="/officer#tab-startup", status_code=307)


@app.get("/research")
@app.get("/research.html")
@app.get("/Research_Methodology_and_Validation.html")
def read_research_methodology():
    """Serve the comprehensive Research Methodology & Validation page."""
    research_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Research_Methodology_and_Validation.html"))
    if os.path.exists(research_path):
        return FileResponse(research_path)
    return RedirectResponse(url="/officer#tab-research")


@app.get("/districts")
def read_districts_portal():
    """Serve the dedicated Monitored Districts & Red Alert Directory webpage."""
    districts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "districts.html"))
    if os.path.exists(districts_path):
        return FileResponse(districts_path)
    return RedirectResponse(url="/user")


@app.get("/districts.html")
def read_districts_html_direct():
    """Serve districts.html directly without losing query parameters."""
    districts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "districts.html"))
    if os.path.exists(districts_path):
        return FileResponse(districts_path)
    return RedirectResponse(url="/districts")

@app.get("/dataset.csv")
def get_dataset_csv():
    """Serve dataset.csv directly over HTTP."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "dataset.csv"))
    if os.path.exists(csv_path):
        return FileResponse(csv_path, media_type="text/csv")
    return RedirectResponse(url="/")


@app.get("/api/health")
def health_check() -> dict:
    """Health check endpoint."""
    predictor_loaded = (
        hasattr(app.state, "predictor")
        and app.state.predictor.model_loaded
    )
    uptime_seconds = int(time.time() - _start_time)
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "uptime_seconds": uptime_seconds,
        "model_loaded": predictor_loaded,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
