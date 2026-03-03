# database/report_db.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

mongo = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo["REPORT_SYSTEM"]

collection = db["admin_settings"]


# Get settings
async def get_settings(chat_id: int):
    data = await collection.find_one({"chat_id": chat_id})
    if not data:
        return {
            "chat_id": chat_id,
            "status": True,
            "staff_group": None,
            "tag_founder": True,
            "tag_admins": True,
            "selected_admins": []
        }
    return data


# Update setting
async def update_setting(chat_id: int, key: str, value):
    await collection.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )


# Set staff group
async def set_staff_group(chat_id: int, staff_group_id: int):
    await collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"staff_group": staff_group_id}},
        upsert=True
    )


# Toggle system
async def toggle_system(chat_id: int):
    data = await get_settings(chat_id)
    new_status = not data.get("status", True)
    await update_setting(chat_id, "status", new_status)
    return new_status
