import time, re, random
from pyrogram.enums import MessageEntityType
from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.mongo.readable_time import get_readable_time
from BrandrdXMusic.mongo.afkdb import add_afk, is_afk, remove_afk


# =========================
# SPOTIFY PROGRESS BAR
# =========================
def make_spotify_bar(length=16):
    filled = random.randint(4, 12)
    return "▰" * filled + "▱" * (length - filled)


# =========================
# AFK COMMAND
# =========================
@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id

    # =========================
    # REMOVE AFK IF ALREADY AFK
    # =========================
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))

            await message.reply_text(
                f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ\n\nᴀᴡᴀʏ ғᴏʀ {seenago}"
            )
        except:
            await message.reply_text(
                f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ"
            )
        return

    # =========================
    # 🎧 SPOTIFY MODE
    # =========================
    if len(message.command) > 2 and message.command[1].lower() == "spotify":
        song_input = message.text.split(None, 2)[2]

        details = {
            "type": "spotify",
            "time": time.time(),
            "data": None,
            "reason": song_input,
        }

        # If replied with photo (album art)
        if message.reply_to_message and message.reply_to_message.photo:
            await app.download_media(
                message.reply_to_message,
                file_name=f"downloads/{user_id}_spotify.jpg",
            )
            details["data"] = "photo"

        # If replied with animation (equalizer gif)
        if message.reply_to_message and message.reply_to_message.animation:
            details["data"] = message.reply_to_message.animation.file_id

        await add_afk(user_id, details)

        await message.reply_text(
            f"🎧 **{message.from_user.first_name}** ɪs ɴᴏᴡ ʟɪsᴛᴇɴɪɴɢ ᴏɴ sᴘᴏᴛɪғʏ"
        )
        return

    # =========================
    # DEFAULT AFK (YOUR OLD LOGIC)
    # =========================
    details = {
        "type": "text",
        "time": time.time(),
        "data": None,
        "reason": None,
    }

    if len(message.command) > 1:
        details["type"] = "text_reason"
        details["reason"] = message.text.split(None, 1)[1][:100]

    await add_afk(user_id, details)
    await message.reply_text(f"{message.from_user.first_name} ɪs ɴᴏᴡ ᴀғᴋ!")


# =========================
# WATCHER
# =========================
@app.on_message(~filters.me & ~filters.bot & ~filters.via_bot, group=1)
async def chat_watcher_func(_, message):

    if message.sender_chat:
        return

    msg = ""

    # Check reply AFK
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        if replied_user:
            verifier, reasondb = await is_afk(replied_user.id)
            if verifier:

                afktype = reasondb["type"]
                reasonafk = reasondb["reason"]
                data = reasondb["data"]
                timeafk = reasondb["time"]
                seenago = get_readable_time(
                    (int(time.time() - timeafk))
                )

                # =========================
                # SPOTIFY DISPLAY
                # =========================
                if afktype == "spotify":

                    bar = make_spotify_bar()

                    caption = (
                        f"🎧 **{replied_user.first_name}** ɪs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ\n\n"
                        f"**{reasonafk}**\n\n"
                        f"`1:12` {bar} `3:24`\n\n"
                        f"💚 ᴏɴ sᴘᴏᴛɪғʏ • ᴀғᴋ sɪɴᴄᴇ {seenago}"
                    )

                    if isinstance(data, str) and data.endswith(".jpg"):
                        await message.reply_photo(
                            photo=f"downloads/{replied_user.id}_spotify.jpg",
                            caption=caption,
                        )
                        return

                    if data and not data.endswith(".jpg"):
                        await message.reply_animation(
                            data,
                            caption=caption,
                        )
                        return

                    await message.reply_text(caption)
                    return

                # =========================
                # NORMAL AFK DISPLAY
                # =========================
                msg += (
                    f"**{replied_user.first_name}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                )

    if msg != "":
        await message.reply_text(msg, disable_web_page_preview=True)
