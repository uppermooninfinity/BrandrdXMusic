import time
import re
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
    # /afk spotify Believer - Imagine Dragons
    # ---------------------------------------------------
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
            await app.download_media(
                message.reply_to_message,
                file_name=f"downloads/{user_id}_spotify.jpg"
            )
            details["data"] = "photo"

        await add_afk(user_id, details)

        await message.reply_text(
            f"🎧 **{message.from_user.first_name}** ɪs ɴᴏᴡ ʟɪsᴛᴇɴɪɴɢ ᴏɴ sᴘᴏᴛɪғʏ"
        )
        return

    # ---------------------------------------------------
    # NORMAL AFK
    # ---------------------------------------------------
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
        f"{message.from_user.first_name} ɪs ɴᴏᴡ ᴀғᴋ!"
    )


# ---------------------------------------------------
# WATCHER
# ---------------------------------------------------
@app.on_message(~filters.me & ~filters.bot, group=1)
async def chat_watcher_func(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Remove AFK if AFK user sends message
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        await message.reply_text(
            f"**{user_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!"
        )
        return

    msg = ""

    # If replying to someone
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_user = message.reply_to_message.from_user
        replied_id = replied_user.id

        verifier, reasondb = await is_afk(replied_id)
        if verifier:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            data = reasondb["data"]
            seenago = get_readable_time(int(time.time() - timeafk))

            # 🎧 Spotify AFK display
            if afktype == "spotify":
                bar = make_spotify_bar()
                caption = (
                    f"🎧 **{replied_user.first_name}** ɪs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ\n\n"
                    f"**{reasonafk}**\n\n"
                    f"`1:12` {bar} `3:24`\n\n"
                    f"💚 ᴏɴ sᴘᴏᴛɪғʏ • ᴀғᴋ sɪɴᴄᴇ {seenago}"
                )

                if data == "photo":
                    await message.reply_photo(
                        photo=f"downloads/{replied_id}_spotify.jpg",
                        caption=caption
                    )
                else:
                    await message.reply_text(caption)
                return

            # Normal AFK
            msg += (
                f"**{replied_user.first_name}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n"
            )
            if reasonafk:
                msg += f"ʀᴇᴀsᴏɴ: `{reasonafk}`"

    # Mention detection
    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntityType.MENTION:
                username = message.text[
                    entity.offset: entity.offset + entity.length
                ].replace("@", "")

                try:
                    user = await app.get_users(username)
                except:
                    continue

                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    reasonafk = reasondb["reason"]
                    data = reasondb["data"]
                    seenago = get_readable_time(
                        int(time.time() - timeafk)
                    )

                    if afktype == "spotify":
                        bar = make_spotify_bar()
                        caption = (
                            f"🎧 **{user.first_name}** ɪs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ\n\n"
                            f"**{reasonafk}**\n\n"
                            f"`0:45` {bar} `3:24`\n\n"
                            f"💚 ᴏɴ sᴘᴏᴛɪғʏ • ᴀғᴋ sɪɴᴄᴇ {seenago}"
                        )

                        if data == "photo":
                            await message.reply_photo(
                                photo=f"downloads/{user.id}_spotify.jpg",
                                caption=caption
                            )
                        else:
                            await message.reply_text(caption)
                        return

                    msg += (
                        f"**{user.first_name}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n"
                    )
                    if reasonafk:
                        msg += f"ʀᴇᴀsᴏɴ: `{reasonafk}`"

    if msg:
        await message.reply_text(msg)
