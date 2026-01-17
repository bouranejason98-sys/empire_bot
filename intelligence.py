from datetime import datetime

class IntelligenceEngine:
    def __init__(self):
        self.business_profiles = {}

    def analyze_message(self, message: str, region: str):
        message_lower = message.lower()

        intent = "general"
        if any(word in message_lower for word in ["price", "cost", "quote"]):
            intent = "pricing"
        elif any(word in message_lower for word in ["book", "appointment", "schedule"]):
            intent = "booking"
        elif any(word in message_lower for word in ["help", "support", "issue"]):
            intent = "support"
        elif any(word in message_lower for word in ["sell", "customers", "leads"]):
            intent = "growth"

        revenue_potential = self.estimate_revenue_potential(intent, region)
        recommendation = self.recommend_service(intent, region)

        return {
            "intent": intent,
            "revenue_potential": revenue_potential,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def estimate_revenue_potential(self, intent, region):
        base = {"pricing":0.7, "booking":0.8, "support":0.6, "growth":0.9, "general":0.5}
        region_multiplier = {"Kenya":0.9, "USA":1.2, "India":0.8, "UK":1.1}
        return round(base.get(intent,0.5) * region_multiplier.get(region,1.0),2)

    def recommend_service(self, intent, region):
        recommendations = {
            "pricing":"Offer automated pricing quotes via WhatsApp.",
            "booking":"Set up automated appointment scheduling.",
            "support":"Deploy customer support automation.",
            "growth":"Launch lead generation and follow-up campaigns.",
            "general":"Start with WhatsApp automation basics."
        }
        return recommendations.get(intent,"Start with WhatsApp automation basics.")


# Public API
engine = IntelligenceEngine()

def route_message(user, message, clone):
    region = clone.get("region","Kenya") if isinstance(clone, dict) else "Kenya"
    result = engine.analyze_message(message, region)
    return {
        "reply": result["recommendation"],
        "intent": result["intent"],
        "confidence": result["revenue_potential"]
    }
