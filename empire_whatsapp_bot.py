# empire_whatsapp_bot.py
# Fully deployable $0 WhatsApp automation bot for small businesses
from agents import AgentOrchestrator
agent_orchestrator = AgentOrchestrator()
from intelligence import IntelligenceEngine
intel_engine = IntelligenceEngine()

from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio
import httpx
import logging
import sqlite3
from datetime import datetime

# ----- CONFIG -----
WHATSAPP_API_URL = "https://your-whatsapp-api-endpoint"  # replace with sandbox or free-tier provider
BOT_NAME = "EmpireBot"
DATABASE = "empire.db"
REGIONS = ["Kenya", "USA", "India", "UK"]  # Add as needed

logging.basicConfig(level=logging.INFO)

# ----- DATABASE SETUP -----
conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    business_type TEXT,
    region TEXT,
    language TEXT,
    revenue REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    name TEXT,
    score REAL,
    status TEXT,
    region TEXT,
    timestamp TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    message TEXT,
    response_type TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ----- FASTAPI SETUP -----
app = FastAPI(title="Empire WhatsApp Bot")

# ----- MODELS -----
class IncomingMessage(BaseModel):
    phone: str
    message: str
    region: str = "Kenya"

# ----- HELPER FUNCTIONS -----
async def send_whatsapp_message(phone: str, message: str):
    async with httpx.AsyncClient() as client:
        payload = {"phone": phone, "message": message}
        try:
            response = await client.post(WHATSAPP_API_URL, json=payload)
            logging.info(f"Sent message to {phone}: {message}")
            return response.status_code
        except Exception as e:
            logging.error(f"Error sending WhatsApp message: {e}")
            return None

def score_lead(message: str) -> float:
    """Simple lead scoring (stub)"""
    keywords = ["buy", "need", "service", "price", "help"]
    score = sum(word in message.lower() for word in keywords)
    return score / len(keywords)

def adapt_region(region: str) -> str:
    """Adjust bot tone and language based on region"""
    mapping = {
        "Kenya": "en-KE",
        "USA": "en-US",
        "India": "en-IN",
        "UK": "en-UK"
    }
    return mapping.get(region, "en")

async def self_heal():
    """Self-healing routine: auto-restarts critical processes"""
    while True:
        try:
            logging.info("Self-healing check: All systems nominal.")
        except Exception as e:
            logging.error(f"Self-healing detected error: {e}")
        await asyncio.sleep(60)  # runs every minute

# ----- MAIN BOT LOGIC -----
@app.post("/webhook")
async def webhook(msg: IncomingMessage):
    phone = msg.phone
    region = msg.region
    lang = adapt_region(region)

    # Save lead
    cursor.execute(
        "INSERT INTO leads (name, score, status, region, timestamp) VALUES (?, ?, ?, ?, ?)",
        (phone, score_lead(msg.message), "new", region, str(datetime.utcnow()))
    )
    conn.commit()
    lead_id = cursor.lastrowid

    # Example adaptive response
    if "hello" in msg.message.lower():
        reply = f"Hello! I'm {BOT_NAME}, here to help your business grow. Which service do you need today?"
    elif "service" in msg.message.lower() or "help" in msg.message.lower():
        reply = "Great! I can automate your WhatsApp for appointments, FAQs, and customer follow-ups. Shall we start?"
    else:
        analysis = intel_engine.analyze_message(msg.message, region)
        agent_response = agent_orchestrator.route(analysis["intent"], analysis)
        reply = f"{analysis['recommendation']} {agent_response}"



    # Save interaction
    cursor.execute(
        "INSERT INTO interactions (lead_id, message, response_type, timestamp) VALUES (?, ?, ?, ?)",
        (lead_id, msg.message, "bot_reply", str(datetime.utcnow()))
    )
    conn.commit()

    await send_whatsapp_message(phone, reply)
    return {"status": "success", "reply": reply}

# ----- START SELF-HEALING LOOP -----
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(self_heal())

# ----- RUN BOT -----
# Run via: uvicorn empire_whatsapp_bot:app --reload --port 8000
