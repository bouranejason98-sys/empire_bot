# analysis_engine.py

def extract_niche(message_lower):
    niches = [
        "real estate", "ecommerce", "healthcare", "education",
        "finance", "restaurants", "law", "construction", "logistics",
        "tourism", "agriculture", "tech"
    ]
    for niche in niches:
        if niche in message_lower:
            return niche
    return "general"


def analyze_message(message, region="Global"):
    message_lower = message.lower()

    if any(word in message_lower for word in ["clone", "duplicate", "replicate", "launch new business"]):
        return {
            "intent": "clone",
            "region": region,
            "niche": extract_niche(message_lower),
            "recommendation": "Deploying a new business clone."
        }

    elif any(word in message_lower for word in ["customer", "customers", "sales", "growth", "leads"]):
        return {
            "intent": "growth",
            "region": region,
            "recommendation": "Launch lead generation and follow-up campaigns."
        }

    elif any(word in message_lower for word in ["support", "help", "issue", "problem"]):
        return {
            "intent": "support",
            "region": region,
            "recommendation": "Connecting you to support services."
        }

    else:
        return {
            "intent": "general",
            "region": region,
            "recommendation": "Start with WhatsApp automation basics."
        }
