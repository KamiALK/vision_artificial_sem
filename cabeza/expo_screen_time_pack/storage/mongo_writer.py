import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "visiondb")
MONGO_COL = os.getenv("MONGO_COL", "screen_time")
_client = MongoClient(MONGO_URI) if MONGO_URI else None


def save_session(session_id: str, roi_points, totals):
    if not _client:
        return False
    db = _client[MONGO_DB]
    col = db[MONGO_COL]
    col.create_index("session_id", unique=True)
    doc = {
        "session_id": session_id,
        "created_at": datetime.utcnow(),
        "roi": [list(map(int, p)) for p in roi_points],
        "totals_sec": {str(k): float(v) for k, v in totals.items()},
    }
    col.update_one({"session_id": session_id}, {"$set": doc}, upsert=True)
    return True
