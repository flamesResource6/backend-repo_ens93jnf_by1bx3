from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Environment variables are provided by the platform
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is not None:
        return _db

    _client = AsyncIOMotorClient(DATABASE_URL)
    _db = _client[DATABASE_NAME]
    return _db


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = await db[collection_name].insert_one(payload)
    return {"_id": str(result.inserted_id), **{k: v for k, v in payload.items()}}


async def get_documents(
    collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50
):
    db = get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        items.append(doc)
    return items
