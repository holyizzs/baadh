"""
Bilingual Emergency Alert Message Templates (English & Hindi).
Formats for SMS (concise <160 chars), WhatsApp (rich format), and IVRS Voice Script.
"""

from typing import Dict, Any


def get_sms_template(district: str, risk_level: str, probability: float, lead_time_hrs: float = 3.5) -> str:
    """Concise SMS message adhering to standard 160-char SMS gateway limits."""
    prob_pct = int(probability * 100) if probability <= 1.0 else int(probability)
    
    if risk_level.upper() in ('SEVERE', 'CRITICAL'):
        lead_str = f"Advance lead time ~{lead_time_hrs}h. " if lead_time_hrs else ""
        return (
            f"EMERGENCY NDMA: Flash Flood RED ALERT for {district}. "
            f"Prob {prob_pct}%. {lead_str}Evacuate low-lying riverbanks immediately. "
            f"Move to high ground. Helpline: 1078."
        )
    elif risk_level.upper() in ('HIGH', 'WARNING'):
        return (
            f"WARNING NDMA: Flash Flood ORANGE ALERT for {district}. "
            f"Prob {prob_pct}%. Lead time {lead_time_hrs}h. Avoid stream crossings. "
            f"Be ready to evacuate. Helpline: 1078."
        )
    else:
        return (
            f"ADVISORY NDMA: Flash Flood WATCH for {district}. "
            f"Prob {prob_pct}%. Rising river discharge. Monitor local channels. "
            f"Helpline: 1070."
        )


def get_whatsapp_template(district: str, state: str, risk_level: str, probability: float, lead_time_hrs: float = 3.5, runoff_mm: float = 0.0) -> str:
    """Rich formatted WhatsApp broadcast message with Hindi translation."""
    prob_pct = round(probability * 100, 1) if probability <= 1.0 else round(probability, 1)
    
    if risk_level.upper() in ('SEVERE', 'CRITICAL'):
        header = "🚨🔴 *आपातकालीन फ्लैश फ्लड चेतावनी / FLASH FLOOD CRITICAL EMERGENCY* 🔴🚨"
        action_en = "MANDATORY EVACUATION: Move families and livestock to designated high-ground shelters immediately. Do NOT attempt to cross causeways or bridges."
        action_hi = "अनिवार्य निकासी: तुरंत ऊंचे सुरक्षित स्थानों पर जाएं। नदी, नालों और पुलों को पार करने की कोशिश न करें।"
    elif risk_level.upper() in ('HIGH', 'WARNING'):
        header = "⚠️🟠 *फ्लैश फ्लड चेतावनी / FLASH FLOOD WARNING ALERT* 🟠⚠️"
        action_en = "BE PREPARED: SDRF & NDRF teams mobilized. Stay away from riverbanks and gorge trails. Keep emergency bags ready."
        action_hi = "तैयार रहें: नदी के किनारों और घाटों से दूर रहें। आपातकालीन सामान तैयार रखें।"
    else:
        header = "ℹ️🟡 *फ्लैश फ्लड निगरानी / FLASH FLOOD WATCH ADVISORY* 🟡ℹ️"
        action_en = "STAY ALERT: Rivers flowing near alert marks. Fishermen and pilgrims advised to avoid low river channels."
        action_hi = "सतर्क रहें: नदियों का जलस्तर बढ़ रहा है। नदी किनारे न जाएं।"

    msg = (
        f"{header}\n\n"
        f"📍 *Location / स्थान:* {district}, {state}\n"
        f"📊 *Flood Probability / बाढ़ की संभावना:* {prob_pct}%\n"
        f"⏳ *Est. Warning Lead Time:* ~{lead_time_hrs} Hours\n"
        f"🌊 *Expected Runoff Volume:* {runoff_mm:.1f} mm\n\n"
        f"👉 *Action Required (English):*\n{action_en}\n\n"
        f"👉 *निर्देश (हिन्दी):*\n{action_hi}\n\n"
        f"📞 *Emergency Contact:* NDMA Control: 1078 | State EOC: 1070\n"
        f"🏛️ *Dispatched by:* Emergency Operation Centre, NDMA Govt. of India"
    )
    return msg


def get_ivrs_voice_script(district: str, risk_level: str, probability: float) -> str:
    """Spoken text for automated emergency IVRS phone call broadcast to DM / Sarpanches."""
    prob_pct = int(probability * 100) if probability <= 1.0 else int(probability)
    
    return (
        f"Attention. This is an urgent priority broadcast from the National Disaster Management Authority. "
        f"A {risk_level} flash flood alert has been issued for {district} district, with an evaluated probability of {prob_pct} percent. "
        f"All river basin authorities, Gram Sarpanches, and emergency teams must immediately initiate public warning and precautionary evacuation. "
        f"Please acknowledge receipt on your terminal. Press 1 to confirm."
    )
