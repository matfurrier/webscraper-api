import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "scraper_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db["scraped_data"]

# Model for data coming from DB (includes id as string)
class ScrapedItemDB(BaseModel):
    id: str = Field(alias="_id")
    fonte: str
    dados: Dict[str, Any]
    data_coleta: datetime

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

# Model for creating new data (id is not included, as MongoDB will generate it)
class ScrapedItemCreate(BaseModel):
    fonte: str
    dados: Dict[str, Any]
    data_coleta: datetime = Field(default_factory=datetime.utcnow)

def save_data(item_create: ScrapedItemCreate) -> str:
    """Saves a single new scraped item to MongoDB."""
    item_dict = item_create.model_dump()
    result = collection.insert_one(item_dict)
    return str(result.inserted_id)

def get_all_data() -> list[ScrapedItemDB]:
    """Retrieves all data from MongoDB."""
    items_from_db = list(collection.find())
    processed_items = []
    for item_db in items_from_db:
        item_db["_id"] = str(item_db["_id"])
        processed_items.append(ScrapedItemDB(**item_db))
    return processed_items

def get_data_by_id(item_id: str) -> ScrapedItemDB | None:
    """Retrieves a single item by its ID from MongoDB."""
    if not ObjectId.is_valid(item_id):
        return None
    item_db = collection.find_one({"_id": ObjectId(item_id)})
    if item_db:
        item_db["_id"] = str(item_db["_id"])
        return ScrapedItemDB(**item_db)
    return None 