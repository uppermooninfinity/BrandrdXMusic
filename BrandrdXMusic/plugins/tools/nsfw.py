import asyncio
from pyrogram import filters
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    add_nsfw,
    remove_nsfw,
    is_nsfw,
    add_nsfw_pack,
    remove_nsfw_pack,
    is_nsfw_pack,
    set_nsfw_status,
    get_nsfw_status,
    get_all_nsfw
)

NSFW_LOGS = -1003700186680  # put your log channel id


# ─────────────────────────────
# NSFW TOGGLE
# ─────────────────────────────

@app.on_message(filters.command("antinsfw") & filters.group)
async def toggle_nsfw(_, message):

    if not message.from_user:
        return

    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if not member.privileges or not member.privileges.can_delete_messages:
        return

    if len(message.command) < 2:
        return await message.reply("Usage: `/antinsfw on|off`")

    arg = message.command[1].lower()

    if arg == "on":
        await set_nsfw_status(message.chat.id, True)
        await message.reply("✅ **NSFW Protection Enabled**")

    elif arg == "off":
        await set_nsfw_status(message.chat.id, False)
        await message.reply("❌ **NSFW Protection Disabled**")


# ─────────────────────────────
# MARK MEDIA NSFW
# ─────────────────────────────

@app.on_message(filters.command("marknsfw") & filters.reply)
async def mark_nsfw(_, message):

    if message.from_user.id not in app.owner_ids:
        return

    media = message.reply_to_message

    file_id = None

    if media.photo:
        file_id = media.photo.file_id

    elif media.video:
        file_id = media.video.file_id

    elif media.sticker:
        file_id = media.sticker.file_id

    if not file_id:
        return await message.reply("Reply to image/video/sticker")

    await add_nsfw(file_id)

    await message.reply("🚫 **Marked as NSFW globally**")


# ─────────────────────────────
# MARK STICKER PACK
# ─────────────────────────────

@app.on_message(filters.command("marksticknsfw") & filters.reply)
async def mark_pack(_, message):

    if message.from_user.id not in app.owner_ids:
        return

    if not message.reply_to_message.sticker:
        return await message.reply("Reply to a sticker")

    pack = message.reply_to_message.sticker.set_name

    await add_nsfw_pack(pack)

    await message.reply("🚫 **Sticker pack blocked globally**")


# ─────────────────────────────
# REMOVE NSFW
# ─────────────────────────────

@app.on_message(filters.command("remark") & filters.reply)
async def remark(_, message):

    if message.from_user.id not in app.owner_ids:
        return

    media = message.reply_to_message

    file_id = None

    if media.photo:
        file_id = media.photo.file_id

    elif media.video:
        file_id = media.video.file_id

    elif media.sticker:
        file_id = media.sticker.file_id

    if not file_id:
        return await message.reply("Reply to NSFW media")

    await remove_nsfw(file_id)

    await message.reply("✅ **Removed from NSFW database**")


# ─────────────────────────────
# NSFW SCAN
# ─────────────────────────────

@app.on_message(filters.command("nsfwscan") & filters.group)
async def scan(_, message):

    if message.from_user.id not in app.owner_ids:
        return

    data = await get_all_nsfw()

    total = len(data)

    await message.reply(
        f"""
**NSFW DATABASE STATS**

🚫 Marked Media : `{total}`

System Status : **Active**
Protection : **Enabled**
"""
    )


# ─────────────────────────────
# AUTO NSFW DELETE
# ─────────────────────────────

@app.on_message(filters.group & (filters.photo | filters.video | filters.sticker))
async def detect_nsfw(_, message):

    status = await get_nsfw_status(message.chat.id)

    if not status:
        return

    file_id = None
    pack = None

    if message.photo:
        file_id = message.photo.file_id

    elif message.video:
        file_id = message.video.file_id

    elif message.sticker:
        file_id = message.sticker.file_id
        pack = message.sticker.set_name

    if file_id and await is_nsfw(file_id):

        await message.delete()

        warn = await message.reply(
            "**ᴄᴏɴᴛᴇɴᴛ ᴅᴇʟᴇᴛᴇᴅ ⚠️**\n\n"
            "> **ᴀᴅᴜʟᴛ / ɴsғᴡ ᴍᴇᴅɪᴀ ɪs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ**\n"
            "> **ɢʀᴏᴜᴘ sᴇᴄᴜʀɪᴛʏ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴀᴄᴛɪᴠᴇ**"
        )

        await asyncio.sleep(6)
        await warn.delete()

        await app.send_message(
            NSFW_LOGS,
            f"NSFW Deleted\nChat: {message.chat.title}\nUser: {message.from_user.id}"
        )

        return

    if pack and await is_nsfw_pack(pack):

        await message.delete()

        warn = await message.reply(
            "**ᴄᴏɴᴛᴇɴᴛ ᴅᴇʟᴇᴛᴇᴅ ⚠️**\n\n"
            "> **ʙʟᴏᴄᴋᴇᴅ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ**\n"
            "> **ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴀᴄᴛɪᴠᴇ**"
        )

        await asyncio.sleep(6)
        await warn.delete()

        await app.send_message(
            NSFW_LOGS,
            f"Sticker Pack Blocked\nChat: {message.chat.title}\nUser: {message.from_user.id}"
        )
