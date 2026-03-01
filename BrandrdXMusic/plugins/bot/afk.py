import os
import time
import random
from pyrogram import filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.mongo.readable_time import get_readable_time
from BrandrdXMusic.mongo.afkdb import add_afk, is_afk, remove_afk

# ---------------------------------------------------
# Spotify Progress Bar
# ---------------------------------------------------
def make_spotify_bar(length=14):
    filled = random.randint(4, 10)
    return "▰" * filled + "▱" * (length - filled)

# ---------------------------------------------------
# SET AFK
# ---------------------------------------------------
@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id

    # Remove AFK if already AFK
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        await message.reply_text(
            f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!"
        )
        return

    # ---------------------------------------------------
    # 🎧 SPOTIFY MODE
    if len(message.command) > 2 and message.command[1].lower() == "spotify":
        song_input = message.text.split(None, 2)[2]

        details = {
            "type": "spotify",
            "time": time.time(),
            "data": None,
            "reason": song_input,
        }

        # If replied with photo → save thumbnail
        if message.reply_to_message and message.reply_to_message.photo:
            thumb_path = f"downloads/{user_id}_spotify.jpg"
            await app.download_media(
                message.reply_to_message.photo, file_name=thumb_path
            )
            details["data"] = "photo"

        await add_afk(user_id, details)

        await message.reply_text(
            f"🎧 **{message.from_user.first_name}** ɪs ɴᴏᴡ ʟɪsᴛᴇɴɪɴɢ ᴏɴ sᴘᴏᴛɪғʏ"
        )
        return

    # ---------------------------------------------------
    # NORMAL AFK
    reason = None
    if len(message.command) > 1:
        reason = message.text.split(None, 1)[1]

    details = {
        "type": "text_reason" if reason else "text",
        "time": time.time(),
        "data": None,
        "reason": reason,
    }

    await add_afk(user_id, details)
    await message.reply_text(
        f"**{message.from_user.first_name}** ɪs ɴᴏᴡ ᴀғᴋ!"
    )

# ---------------------------------------------------
# WATCHER
# ---------------------------------------------------
@app.on_message(~filters.me & ~filters.bot, group=1)
async def chat_watcher_func(_, message: Message):
    if message.sender_chat:
        return

    msg = ""

    # 1️⃣ Check if the sender themselves were AFK → remove
    verifier, reasondb = await is_afk(message.from_user.id)
    if verifier:
        await remove_afk(message.from_user.id)
        await message.reply_text(
            f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!"
        )
        return

    # 2️⃣ Check if replying to someone AFK
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_user = message.reply_to_message.from_user
        verifier, reasondb = await is_afk(replied_user.id)
        if verifier:
            await send_afk_message(message, replied_user, reasondb)
            return

    # 3️⃣ Check mentions
    if message.entities:
        for entity in message.entities:
            user = None
            if entity.type == MessageEntityType.MENTION:
                username = message.text[entity.offset: entity.offset + entity.length].replace("@", "")
                try:
                    user = await app.get_users(username)
                except:
                    continue
            elif entity.type == MessageEntityType.TEXT_MENTION:
                user = entity.user

            if not user:
                continue

            verifier, reasondb = await is_afk(user.id)
            if verifier:
                await send_afk_message(message, user, reasondb)
                return

async def send_afk_message(message: Message, user, reasondb):
    afktype = reasondb["type"]
    timeafk = reasondb["time"]
    reasonafk = reasondb["reason"]
    data = reasondb["data"]
    seenago = get_readable_time(int(time.time() - timeafk))

    if afktype == "spotify":
        bar = make_spotify_bar()
        caption = (
            f"🎧 **{user.first_name}** ɪs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ\n\n"
            f"**{reasonafk}**\n\n"
            f"`0:45` {bar} `3:24`\n\n"
            f"💚 ᴏɴ sᴘᴏᴛɪғʏ • ᴀғᴋ sɪɴᴄᴇ {seenago}"
        )

        photo_path = f"downloads/{user.id}_spotify.jpg"
        if data == "photo" and os.path.exists(photo_path):
            await message.reply_photo(photo=photo_path, caption=caption)
        else:
            await message.reply_text(caption)
        return

    # Normal AFK
    msg = f"**{user.first_name}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}"
    if reasonafk:
        msg += f"\nʀᴇᴀsᴏɴ: `{reasonafk}`"
    await message.reply_text(msg)
