# app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, MASTER_DB

client = AsyncIOMotorClient(MONGO_URI)
master_db = client[MASTER_DB]
# We will use `client` to get per-org DB/collection (dynamic)
