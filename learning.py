from memory_engine import MemoryEngine

class LearningEngine:
    def __init__(self):
        self.memory = MemoryEngine()

    def improve_response(self, user, clone):
        memory = self.memory.recall(user, clone)
        if not memory:
            return None

        intent = memory["intent"]
        confidence = memory["confidence"]

        if confidence < 0.6:
            return "Would you like a human agent to assist you?"
        elif intent == "pricing":
            return "Would you like a custom quote tailored to your needs?"
        elif intent == "booking":
            return "Can I help you schedule that now?"
        return None
