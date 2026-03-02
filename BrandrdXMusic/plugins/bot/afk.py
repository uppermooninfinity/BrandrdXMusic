import os
import time
import random
from pyrogram import filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from BrandrdXMusic import app
from BrandrdXMusic.mongo.readable_time import get_readable_time
from BrandrdXMusic.mongo.afkdb import add_afk, is_afk, remove_afk

DEVELOPER_URL = "https://t.me/cyber_github"  # change this

# ---------------------------------------------------
# Spotify Progress Bar
# ---------------------------------------------------
def make_spotify_bar(length=14):
    filled = random.randint(4, 10)
    return "▰" * filled + "▱" * (length - filled)


def spotify_buttons(bar):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• ʟɪꜱᴛᴇɴ ᴏɴ sᴘᴏᴛɪғʏ •",
                    url="https://open.spotify.com/",
                )
            ],
            [
                InlineKeyboardButton(
                    f"0:45 {bar} 3:24",
                    callback_data="afk_progress",
                )
            ],
            [
                InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url=DEVELOPER_URL),
                InlineKeyboardButton("• ᴄʟᴏꜱᴇ •", callback_data="afk_close"),
            ],
        ]
    )


# ---------------------------------------------------
# SET AFK
# ---------------------------------------------------
@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id

    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        await message.reply_text(
            f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!"
        )
        return

    # 🎧 SPOTIFY MODE
    if len(message.command) > 2 and message.command[1].lower() == "spotify":
        song_input = message.text.split(None, 2)[2]

        details = {
            "type": "spotify",
            "time": time.time(),
            "data": None,
            "reason": song_input,
        }

        # Save GIF if replied
        if message.reply_to_message and message.reply_to_message.animation:
            os.makedirs("downloads", exist_ok=True)
            gif_path = f"downloads/{user_id}_spotify.gif"
            await app.download_media(
                message.reply_to_message.animation, file_name=gif_path
            )
            details["data"] = "gif"

        await add_afk(user_id, details)

        bar = make_spotify_bar()
        caption = (
            f"🎧 **{message.from_user.first_name}** ɪs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ\n\n"
            f"**{song_input.lower()}**\n\n"
            f"💚 ᴏɴ sᴘᴏᴛɪғʏ"
        )

        await message.reply_text(
            caption,
            reply_markup=spotify_buttons(bar),
        )
        return

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

    # Remove AFK if sender returns
    verifier, reasondb = await is_afk(message.from_user.id)
    if verifier:
        await remove_afk(message.from_user.id)
        await message.reply_text(
            f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!"
        )
        return

    # Reply check
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_user = message.reply_to_message.from_user
        verifier, reasondb = await is_afk(replied_user.id)
        if verifier:
            await send_afk_message(message, replied_user, reasondb)
            return

    # Mention check
    if message.entities:
        for entity in message.entities:
            user = None
            if entity.type == MessageEntityType.MENTION:
                username = message.text[
                    entity.offset : entity.offset + entity.length
                ].replace("@", "")
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


# ---------------------------------------------------
# SEND AFK MESSAGE
# ---------------------------------------------------
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
            f"**{reasonafk.lower()}**\n\n"
            f"💚 ᴏɴ sᴘᴏᴛɪғʏ • ᴀғᴋ sɪɴᴄᴇ {seenago}"
        )

        gif_path = f"downloads/{user.id}_spotify.gif"

        if data == "gif" and os.path.exists(gif_path):
            await message.reply_animation(
                animation=gif_path,
                caption=caption,
                reply_markup=spotify_buttons(bar),
            )
        else:
            await message.reply_text(
                caption,
                reply_markup=spotify_buttons(bar),
            )
        return

    msg = f"**{user.first_name}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}"
    if reasonafk:
        msg += f"\nʀᴇᴀsᴏɴ: `{reasonafk}`"
    await message.reply_text(msg)


# ---------------------------------------------------
# CALLBACK HANDLERS
# ---------------------------------------------------
@app.on_callback_query(filters.regex("afk_close"))
async def close_afk(_, query: CallbackQuery):
    await query.message.delete()


@app.on_callback_query(filters.regex("afk_progress"))
async def progress_ignore(_, query: CallbackQuery):
    await query.answer("🎧 ᴘʟᴀʏɪɴɢ...", show_alert=False)
