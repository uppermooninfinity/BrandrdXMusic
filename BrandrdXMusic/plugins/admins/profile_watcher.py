import html

from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_profile, save_profile


@app.on_message(filters.group & filters.incoming)
async def profile_watcher(client, message: Message):

    user = message.from_user
    if not user or user.is_bot:
        return

    user_id = user.id

    # Current data
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    username = f"@{user.username}" if user.username else "None"

    # Fetch fresh bio
    try:
        fresh = await client.get_users(user_id)
        bio = fresh.bio or "None"
    except Exception:
        bio = "None"

    current_data = {
        "name": full_name.strip(),
        "username": username.strip(),
        "bio": bio.strip()
    }

    old_data = await get_profile(user_id)

    # First time → just store
    if not old_data:
        await save_profile(user_id, current_data)
        return

    changes = []

    # Strict comparison (even dot change detected)
    if old_data.get("name", "").strip() != current_data["name"]:
        changes.append(
            f"<b>👤 Name Changed</b>\n"
            f"Old: {html.escape(old_data.get('name','None'))}\n"
            f"New: {html.escape(current_data['name'])}\n"
        )

    if old_data.get("username", "").strip() != current_data["username"]:
        changes.append(
            f"<b>🔗 Username Changed</b>\n"
            f"Old: {html.escape(old_data.get('username','None'))}\n"
            f"New: {html.escape(current_data['username'])}\n"
        )

    if old_data.get("bio", "").strip() != current_data["bio"]:
        changes.append(
            f"<b>📝 Bio Changed</b>\n"
            f"Old: {html.escape(old_data.get('bio','None'))}\n"
            f"New: {html.escape(current_data['bio'])}\n"
        )

    if changes:
        text = (
            f"⚡ <b>PROFILE UPDATED</b>\n\n"
            f"<b>User:</b> {user.mention}\n\n"
            + "\n".join(changes)
        )

        await message.reply(text, disable_web_page_preview=True)

    # Always update stored data
    await save_profile(user_id, current_data)
