import html
from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic..profile_tracker import get_user, save_user


@app.on_message(filters.group & filters.incoming)
async def profile_watcher(client, message: Message):

    user = message.from_user
    if not user:
        return

    user_id = user.id

    # Current details
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    username = f"@{user.username}" if user.username else "None"

    full_name = f"{first_name} {last_name}".strip()

    # Fetch bio
    try:
        full_user = await client.get_users(user_id)
        bio = full_user.bio or "None"
    except Exception:
        bio = "None"

    current_data = {
        "name": full_name,
        "username": username,
        "bio": bio
    }

    old_data = await get_user(user_id)

    # First time → just save
    if not old_data:
        await save_user(user_id, current_data)
        return

    changes = []

    if old_data.get("name") != current_data["name"]:
        changes.append(
            f"<b>Name Changed:</b>\n"
            f"Old: {html.escape(old_data.get('name','None'))}\n"
            f"New: {html.escape(current_data['name'])}\n"
        )

    if old_data.get("bio") != current_data["bio"]:
        changes.append(
            f"<b>Bio Changed:</b>\n"
            f"Old: {html.escape(old_data.get('bio','None'))}\n"
            f"New: {html.escape(current_data['bio'])}\n"
        )

    if old_data.get("username") != current_data["username"]:
        changes.append(
            f"<b>Username Changed:</b>\n"
            f"Old: {html.escape(old_data.get('username','None'))}\n"
            f"New: {html.escape(current_data['username'])}\n"
        )

    if changes:
        text = (
            f"⚡ <b>Profile Update Detected</b>\n\n"
            f"<b>User:</b> {user.mention}\n\n"
            + "\n".join(changes)
        )

        await message.reply(text)

    # Update database
    await save_user(user_id, current_data)
