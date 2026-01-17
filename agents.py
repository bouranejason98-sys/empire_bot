# agents.py

from datetime import datetime
import random
import logging

logging.basicConfig(level=logging.INFO)

class BaseAgent:
    name = "BaseAgent"

    def can_handle(self, intent):
        return False

    def handle(self, context):
        return f"{self.name} processed the task."

class SalesAgent(BaseAgent):
    name = "SalesAgent"

    def can_handle(self, intent):
        return intent in ["pricing", "growth"]

    def handle(self, context):
        return "Our SalesAgent is preparing a custom offer for your business."

class SupportAgent(BaseAgent):
    name = "SupportAgent"

    def can_handle(self, intent):
        return intent == "support"

    def handle(self, context):
        return "Our SupportAgent is resolving your issue. A solution is on the way."

class GrowthAgent(BaseAgent):
    name = "GrowthAgent"

    def can_handle(self, intent):
        return intent == "growth"

    def handle(self, context):
        return "Our GrowthAgent is optimizing your lead generation and conversion systems."

class SystemAgent(BaseAgent):
    name = "SystemAgent"

    def can_handle(self, intent):
        return intent == "system"

    def handle(self, context):
        return "System health check complete. All systems stable."

class AgentOrchestrator:
    def __init__(self):
        self.agents = [
            SalesAgent(),
            SupportAgent(),
            GrowthAgent(),
            SystemAgent()
        ]

    def route(self, intent, context):
        for agent in self.agents:
            if agent.can_handle(intent):
                return agent.handle(context)
        return "No agent found. A human operator will review this request."
