"""
Official Emergency Contact & Person of Contact (POC) Directory.
Organized by administrative hierarchy:
- Tier 1: District Magistrate (DM), Superintendent of Police (SP), NDRF Commandant
- Tier 2: Sub-Divisional Magistrate (SDM), Block Development Officer (BDO), Gram Sarpanch
- Tier 3: Local Community Watch & Siren Nodes
"""

from typing import Dict, List, Any, Optional

POC_DIRECTORY: Dict[str, Dict[str, Any]] = {
    'Rudraprayag': {
        'state': 'Uttarakhand',
        'eoc_phone': '01364-233727',
        'siren_node_id': 'SIREN-RP-01',
        'registered_residents': 540,
        'officials': [
            {
                'role': 'District Magistrate (DM)',
                'name': 'DM Rudraprayag',
                'phone': '+91-9412000001',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'NDRF 8th Battalion Commandant',
                'name': 'Commandant NDRF Garhwal',
                'phone': '+91-9412000002',
                'tier': 1,
                'channels': ['whatsapp', 'sms']
            },
            {
                'role': 'Kedarnath Gram Sarpanch',
                'name': 'Sarpanch Kedarnath Ghati',
                'phone': '+91-9412000003',
                'tier': 2,
                'channels': ['call', 'sms']
            },
            {
                'role': 'BDO Ukhimath',
                'name': 'Block Development Officer',
                'phone': '+91-9412000004',
                'tier': 2,
                'channels': ['sms', 'whatsapp']
            }
        ]
    },
    'Chamoli': {
        'state': 'Uttarakhand',
        'eoc_phone': '01372-251437',
        'siren_node_id': 'SIREN-CH-02',
        'registered_residents': 480,
        'officials': [
            {
                'role': 'District Magistrate (DM)',
                'name': 'DM Chamoli',
                'phone': '+91-9412000011',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Joshimath Sub-Divisional Magistrate',
                'name': 'SDM Joshimath',
                'phone': '+91-9412000012',
                'tier': 2,
                'channels': ['call', 'sms']
            },
            {
                'role': 'Raini/Tapovan Village Pradhan',
                'name': 'Gram Pradhan Tapovan',
                'phone': '+91-9412000013',
                'tier': 2,
                'channels': ['call', 'sms']
            }
        ]
    },
    'Uttarkashi': {
        'state': 'Uttarakhand',
        'eoc_phone': '01374-222722',
        'siren_node_id': 'SIREN-UK-03',
        'registered_residents': 390,
        'officials': [
            {
                'role': 'District Magistrate (DM)',
                'name': 'DM Uttarkashi',
                'phone': '+91-9412000021',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Bhatwari Gram Pradhan',
                'name': 'Pradhan Bhatwari',
                'phone': '+91-9412000022',
                'tier': 2,
                'channels': ['call', 'sms']
            }
        ]
    },
    'Kullu': {
        'state': 'Himachal Pradesh',
        'eoc_phone': '01902-225630',
        'siren_node_id': 'SIREN-KL-04',
        'registered_residents': 620,
        'officials': [
            {
                'role': 'Deputy Commissioner (DC)',
                'name': 'DC Kullu',
                'phone': '+91-9418000031',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Manali SDM',
                'name': 'SDM Manali',
                'phone': '+91-9418000032',
                'tier': 2,
                'channels': ['call', 'sms']
            }
        ]
    },
    'Mandi': {
        'state': 'Himachal Pradesh',
        'eoc_phone': '01905-226201',
        'siren_node_id': 'SIREN-MD-05',
        'registered_residents': 510,
        'officials': [
            {
                'role': 'Deputy Commissioner (DC)',
                'name': 'DC Mandi',
                'phone': '+91-9418000041',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Pandoh Dam Emergency Officer',
                'name': 'Executive Engineer BBMB',
                'phone': '+91-9418000042',
                'tier': 1,
                'channels': ['call', 'whatsapp']
            }
        ]
    },
    'Mangan': {
        'state': 'Sikkim',
        'eoc_phone': '03592-234201',
        'siren_node_id': 'SIREN-MG-06',
        'registered_residents': 320,
        'officials': [
            {
                'role': 'District Collector (DC)',
                'name': 'DC Mangan North Sikkim',
                'phone': '+91-9434000051',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Chungthang Sub-Divisional Magistrate',
                'name': 'SDM Chungthang',
                'phone': '+91-9434000052',
                'tier': 2,
                'channels': ['call', 'sms']
            }
        ]
    },
    'Leh': {
        'state': 'Ladakh',
        'eoc_phone': '01982-255555',
        'siren_node_id': 'SIREN-LH-07',
        'registered_residents': 280,
        'officials': [
            {
                'role': 'Deputy Commissioner (DC)',
                'name': 'DC Leh',
                'phone': '+91-9419000061',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'UT Disaster Management Officer',
                'name': 'DDMA Coordinator Ladakh',
                'phone': '+91-9419000062',
                'tier': 1,
                'channels': ['call', 'sms']
            }
        ]
    },
    'Cherrapunji': {
        'state': 'Meghalaya',
        'eoc_phone': '0364-2502094',
        'siren_node_id': 'SIREN-CP-08',
        'registered_residents': 350,
        'officials': [
            {
                'role': 'Deputy Commissioner',
                'name': 'DC East Khasi Hills',
                'phone': '+91-9436000071',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Sohra Block Development Officer',
                'name': 'BDO Sohra',
                'phone': '+91-9436000072',
                'tier': 2,
                'channels': ['sms', 'whatsapp']
            }
        ]
    }
}


def get_pocs_for_district(district: str) -> Dict[str, Any]:
    """Retrieve POCs and emergency node info for a specific district with safe fallback."""
    if district in POC_DIRECTORY:
        return POC_DIRECTORY[district]
    
    # Generic Himalayan fallback
    return {
        'state': 'Himalayan Zone',
        'eoc_phone': '1070',
        'siren_node_id': f'SIREN-GEN-01',
        'registered_residents': 300,
        'officials': [
            {
                'role': 'District Disaster Management Officer',
                'name': f'DDMO {district}',
                'phone': '+91-9876543210',
                'tier': 1,
                'channels': ['call', 'whatsapp', 'sms']
            },
            {
                'role': 'Sub-Divisional Magistrate (SDM)',
                'name': f'SDM {district}',
                'phone': '+91-9876543211',
                'tier': 2,
                'channels': ['call', 'sms']
            },
            {
                'role': 'Local Gram Panchayat Sarpanch',
                'name': 'Head Sarpanch',
                'phone': '+91-9876543212',
                'tier': 2,
                'channels': ['sms', 'call']
            }
        ]
    }
