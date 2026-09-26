import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.alert_service import dispatch_alert
from app.services.push_service import (
    register_device, unregister_device, get_registered_devices,
    firebase_status, send_push_alert, CRITICAL_CHANNEL_ID
)
from app.services.poc_directory import POC_DIRECTORY, get_pocs_for_district

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for alerts history (last 50 alerts)
_alerts_history: List[Dict[str, Any]] = [
    {
        'id': 'AL_20260923_104500_001',
        'village': 'Kedarnath',
        'risk_level': 'SEVERE',
        'probability': 0.885,
        'message': 'EMERGENCY NDMA: Flash Flood RED ALERT for Kedarnath. Evacuate immediately.',
        'channels': ['sms', 'whatsapp', 'call', 'siren'],
        'issued_at': '2026-09-23T10:45:00Z',
        'delivery_stats': {'channels': {'bulk_community_sms': {'delivered': 540}, 'siren': {'activated': True}}}
    },
    {
        'id': 'AL_20260923_111500_002',
        'village': 'Rudraprayag',
        'risk_level': 'HIGH',
        'probability': 0.720,
        'message': 'WARNING NDMA: Flash Flood ORANGE ALERT for Rudraprayag. Lead time 3.5h.',
        'channels': ['sms', 'whatsapp', 'call'],
        'issued_at': '2026-09-23T11:15:00Z',
        'delivery_stats': {'channels': {'bulk_community_sms': {'delivered': 480}, 'siren': {'activated': False}}}
    }
]


class AlertRequest(BaseModel):
    pin: str = Field(..., description='Security PIN to authorize alert dispatch (e.g. 1078)')
    village: str = Field(..., description='Target district or valley region')
    risk_level: str = Field(default='HIGH', description='Risk level: MODERATE, HIGH, SEVERE')
    probability: float = Field(default=0.75, description='Probability of flash flood (0.0 to 1.0)')
    channels: List[str] = Field(default=['sms', 'whatsapp', 'call', 'siren', 'push'], description='Dispatch channels')
    lead_time_hrs: float = Field(default=7.5, description='Estimated forecast lead time in hours (default 7.5h for severe alerts)')
    custom_recipient: Optional[str] = Field(default=None, description='Optional phone number for live testing')
    gateway_url: Optional[str] = Field(default="http://192.168.43.1:8080", description='Local Android SMS gateway URL')
    relay_mode: Optional[str] = Field(default="AUTO", description='Relay mode: AUTO, ANDROID_HOTSPOT, CLOUD')
    bypass_cooldown: bool = Field(default=True, description='Bypass 30-min duplicate cooldown for demo overrides')


class TestAlertRequest(BaseModel):
    pin: str = Field(..., description='Security PIN (1078)')
    phone_number: str = Field(..., description='Phone number to send live test alert (e.g. +919876543210)')
    district: str = Field(default='Rudraprayag', description='Sample district for alert template')
    risk_level: str = Field(default='HIGH', description='Sample risk level: HIGH or SEVERE')
    gateway_url: Optional[str] = Field(default="http://192.168.43.1:8080", description='Local Android SMS gateway URL')
    relay_mode: Optional[str] = Field(default="AUTO", description='Relay mode: AUTO, ANDROID_HOTSPOT, CLOUD')


class AlertResponse(BaseModel):
    success: bool
    alert_id: str
    message: str
    delivery_stats: Dict[str, Any]
    issued_at: str


@router.post('/alerts/send', response_model=AlertResponse)
async def send_alert(data: AlertRequest) -> AlertResponse:
    """Send an emergency flash flood alert to POCs and residents."""
    if data.pin != '1078':
        logger.warning(f'Unauthorized alert attempt for region {data.village} with PIN: {data.pin}')
        raise HTTPException(status_code=401, detail='Invalid authorization PIN. Security check failed.')
    
    try:
        now = datetime.now(timezone.utc)
        alert_id = f'ALERT_{now.strftime("%Y%m%d_%H%M%S")}_{len(_alerts_history)+1:03d}'
        
        # Dispatch through orchestrator
        delivery_stats = dispatch_alert(
            village=data.village,
            risk_level=data.risk_level,
            probability=data.probability,
            channels=data.channels,
            lead_time_hrs=data.lead_time_hrs,
            custom_recipient=data.custom_recipient,
            bypass_cooldown=data.bypass_cooldown,
            gateway_url=data.gateway_url or "http://192.168.43.1:8080",
            relay_mode=data.relay_mode or "AUTO"
        )
        
        from app.services.alert_templates import get_sms_template
        message = get_sms_template(data.village, data.risk_level, data.probability, data.lead_time_hrs)
        
        alert_record = {
            'id': alert_id,
            'village': data.village,
            'risk_level': data.risk_level.upper(),
            'probability': data.probability,
            'message': message,
            'channels': data.channels,
            'issued_at': now.isoformat(),
            'delivery_stats': delivery_stats
        }
        
        # Keep last 50 alerts in history
        _alerts_history.insert(0, alert_record)
        if len(_alerts_history) > 50:
            _alerts_history.pop()
            
        logger.info(f'Alert {alert_id} successfully dispatched to {data.village} across {data.channels}')
        
        return AlertResponse(
            success=True,
            alert_id=alert_id,
            message=f'Emergency alert successfully authorized and dispatched to {data.village}',
            delivery_stats=delivery_stats,
            issued_at=now.isoformat()
        )
    except Exception as e:
        logger.error(f'Failed to dispatch alert: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Failed to dispatch alert: {str(e)}')


@router.post('/alerts/test')
async def test_alert_to_phone(data: TestAlertRequest) -> Dict[str, Any]:
    """Test send a live flash flood alert to a specific evaluator or officer phone number."""
    if data.pin != '1078':
        raise HTTPException(status_code=401, detail='Invalid security PIN')
        
    res = dispatch_alert(
        village=data.district,
        risk_level=data.risk_level,
        probability=0.82,
        channels=['sms', 'whatsapp'],
        custom_recipient=data.phone_number,
        bypass_cooldown=True,
        gateway_url=data.gateway_url or "http://192.168.43.1:8080",
        relay_mode=data.relay_mode or "AUTO"
    )
    return {
        'success': True,
        'recipient': data.phone_number,
        'district': data.district,
        'dispatch_result': res
    }


@router.get('/alerts/history')
async def get_alerts_history() -> Dict[str, Any]:
    """Retrieve the real-time history of issued alerts (last 50)."""
    return {
        'success': True,
        'count': len(_alerts_history),
        'alerts': _alerts_history,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }


@router.get('/alerts/push/status')
async def push_status() -> Dict[str, Any]:
    """Firebase FCM configuration and registered mobile devices."""
    return {'success': True, **firebase_status(), 'devices': get_registered_devices()}


class DeviceRegistration(BaseModel):
    token: str = Field(..., min_length=10, description='FCM registration token from the mobile PWA')
    district: str = Field(default='ALL', description='District to subscribe: e.g. Rudraprayag, Chamoli, or ALL')
    label: str = Field(default='', description='Optional device label, e.g. "SDRF Phone 1"')


@router.post('/alerts/register-device')
async def register_push_device(data: DeviceRegistration) -> Dict[str, Any]:
    """Register a mobile device's FCM token for flood alert beeps."""
    res = register_device(data.token, data.district, data.label)
    if not res.get('success'):
        raise HTTPException(status_code=400, detail=res.get('error', 'Registration failed'))
    return res


@router.post('/alerts/unregister-device')
async def unregister_push_device(data: DeviceRegistration) -> Dict[str, Any]:
    """Remove a device's FCM token (called on unsubscribe)."""
    return unregister_device(data.token)


@router.post('/alerts/push/test')
async def send_test_push(data: DeviceRegistration) -> Dict[str, Any]:
    """Fire a sample flood-alert push to ONE device token (end-to-end beep test)."""
    res = send_push_alert(
        district=data.district,
        risk_level='SEVERE',
        probability=0.9,
        lead_time_hrs=7.5,
        tokens=[data.token]
    )
    return {'success': res.get('success', False), 'district': data.district, 'result': res}


@router.get('/alerts/pocs')
async def get_pocs(district: Optional[str] = Query(None, description='Filter by district')) -> Dict[str, Any]:
    """Retrieve POC contact directory for officials and village responders."""
    if district:
        info = get_pocs_for_district(district)
        return {
            'success': True,
            'district': district,
            'directory': info
        }
    return {
        'success': True,
        'total_districts': len(POC_DIRECTORY),
        'districts': POC_DIRECTORY
    }


# =========================================================================
# OFFLINE EMERGENCY CELLULAR BROADCAST (ZERO-INTERNET DEMONSTRATION)
# =========================================================================

from app.services.offline_sms_relay import (
    load_team_directory,
    save_team_directory,
    ping_relay_gateway,
    dispatch_offline_team_alert
)


class TeamMemberModel(BaseModel):
    id: Optional[str] = None
    name: str
    role: str
    phone: str
    active: bool = True


class OfflineAlertRequest(BaseModel):
    pin: str = Field(..., description="Security PIN (1078)")
    village: str = Field(default="Kedarnath", description="Target district or valley")
    risk_level: str = Field(default="SEVERE", description="MODERATE, HIGH, SEVERE")
    custom_message: Optional[str] = Field(default=None, description="Optional custom message")
    gateway_url: str = Field(default="http://192.168.43.1:8080", description="Android SMS bridge IP/Port")
    mode: str = Field(default="AUTO", description="AUTO, ANDROID_HOTSPOT, USB_SERIAL, SIMULATOR")
    com_port: str = Field(default="COM3", description="COM Port for USB GSM Modem")
    recipients: Optional[List[Dict[str, Any]]] = Field(default=None, description="Recipients list")


@router.get('/alerts/team-directory')
async def get_team_directory() -> Dict[str, Any]:
    """Get registered team members for offline broadcast."""
    members = load_team_directory()
    return {
        'success': True,
        'count': len(members),
        'team': members
    }


@router.post('/alerts/team-directory')
async def update_team_directory(members: List[TeamMemberModel]) -> Dict[str, Any]:
    """Save or update team members list."""
    data = [m.dict() for m in members]
    for i, item in enumerate(data):
        if not item.get('id'):
            item['id'] = f"TM_{i+1:02d}"
    saved = save_team_directory(data)
    if not saved:
        raise HTTPException(status_code=500, detail="Failed to save team directory.")
    return {
        'success': True,
        'count': len(data),
        'team': data,
        'message': 'Team directory updated successfully.'
    }


@router.get('/alerts/offline-relay/status')
async def check_offline_relay_status(url: str = Query('http://192.168.43.1:8080')) -> Dict[str, Any]:
    """Ping local Android SMS bridge or USB modem status over offline subnet."""
    status = ping_relay_gateway(url)
    return status


@router.post('/alerts/offline-team-dispatch')
async def trigger_offline_team_dispatch(data: OfflineAlertRequest) -> Dict[str, Any]:
    """
    Dispatch emergency SMS alert to all registered team members without requiring an active internet connection.
    Uses local offline Wi-Fi hotspot bridge to Android phone's cellular SIM or USB GSM Modem.
    """
    if data.pin != '1078':
        logger.warning(f"Unauthorized offline dispatch attempt with PIN: {data.pin}")
        raise HTTPException(status_code=401, detail="Invalid security PIN. Authorization denied.")
        
    try:
        result = dispatch_offline_team_alert(
            village=data.village,
            risk_level=data.risk_level,
            custom_message=data.custom_message,
            gateway_url=data.gateway_url,
            mode=data.mode,
            com_port=data.com_port,
            recipients=data.recipients
        )
        
        # Add to alert history log for the dashboard
        now = datetime.now(timezone.utc)
        alert_record = {
            'id': f"OFFLINE_GSM_{now.strftime('%Y%m%d_%H%M%S')}",
            'village': data.village,
            'risk_level': data.risk_level.upper(),
            'probability': 0.94,
            'message': result.get('message', ''),
            'channels': ['offline_cellular_sms'],
            'issued_at': now.isoformat(),
            'delivery_stats': {
                'channels': {
                    'offline_gsm_sms': {
                        'delivered': result.get('delivered', 0),
                        'failed': result.get('failed', 0),
                        'mode': result.get('mode_executed'),
                        'gateway': data.gateway_url
                    }
                }
            }
        }
        _alerts_history.insert(0, alert_record)
        if len(_alerts_history) > 50:
            _alerts_history.pop()
            
        return result
    except Exception as e:
        logger.error(f"Offline dispatch failure: {e}")
        raise HTTPException(status_code=500, detail=f"Offline broadcast error: {str(e)}")

