import html
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_profile, save_profile


# Cooldown cache (avoid heavy get_users spam)
_last_checked = {}
COOLDOWN = 300  # 5 minutes


@app.on_message(filters.group & filters.incoming)
async def profile_watcher(client, message: Message):

    user = message.from_user
    if not user or user.is_bot:
        return

    user_id = user.id
    chat_id = message.chat.id

    # Cooldown check
    now = asyncio.get_event_loop().time()
    if user_id in _last_checked:
        if now - _last_checked[user_id] < COOLDOWN:
            return
    _last_checked[user_id] = now

    # Current visible data
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    username = f"@{user.username}" if user.username else "None"

    # Fetch bio safely
    try:
        full_user = await client.get_users(user_id)
        bio = full_user.bio or "None"
    except Exception:
        bio = "None"

    current_data = {
        "name": full_name,
        "username": username,
        "bio": bio,
    }

    old_data = await get_profile(user_id)

    # First appearance → just store
    if not old_data:
        await save_profile(user_id, current_data)
        return

    changes = []

    if old_data.get("name") != current_data["name"]:
        changes.append(
            f"<b>👤 Name Changed</b>\n"
            f"Old: {html.escape(old_data.get('name','None'))}\n"
            f"New: {html.escape(current_data['name'])}\n"
        )

    if old_data.get("username") != current_data["username"]:
        changes.append(
            f"<b>🔗 Username Changed</b>\n"
            f"Old: {html.escape(old_data.get('username','None'))}\n"
            f"New: {html.escape(current_data['username'])}\n"
        )

    if old_data.get("bio") != current_data["bio"]:
        changes.append(
            f"<b>📝 Bio Changed</b>\n"
            f"Old: {html.escape(old_data.get('bio','None'))}\n"
            f"New: {html.escape(current_data['bio'])}\n"
        )

    if changes:
        alert_text = (
            f"⚡ <b>Profile Update Detected</b>\n\n"
            f"<b>User:</b> {user.mention}\n\n"
            + "\n".join(changes)
        )

        await message.reply(alert_text, disable_web_page_preview=True)

    # Update database
    await save_profile(user_id, current_data)
