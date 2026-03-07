from pyrogram import filters
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    get_antiflood_settings,
    set_flood_threshold,
    set_flood_timer,
    set_flood_action,
    set_delete_flood_messages,
    set_flood_action_duration,
    get_flood_action_duration
)

flood_tracker = {}


# ─────────────────────────────
# ADMIN CHECK
# ─────────────────────────────

async def is_admin(chat_id, user_id):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]


# ─────────────────────────────
# SHOW SETTINGS
# ─────────────────────────────

@app.on_message(filters.command("flood") & filters.group)
async def flood_settings(_, message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return

    settings = await get_antiflood_settings(message.chat.id)

    if settings["flood_threshold"] == 0:
        return await message.reply_text(
            "**⚠️ 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝗂𝗌 𝖢𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**"
        )

    await message.reply_text(
        f"""
**🛡️ 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌**

• 𝖳𝗁𝗋𝖾𝗌𝗁𝗈𝗅𝖽 : `{settings["flood_threshold"]}` messages  
• 𝖳𝗂𝗆𝖾𝖽 : `{settings["flood_timer_count"]}` msgs / `{settings["flood_timer_duration"]}s`  
• 𝖠𝖼𝗍𝗂𝗈𝗇 : `{settings["flood_action"]}`  
• 𝖣𝖾𝗅𝖾𝗍𝖾 𝖬𝗌𝗀𝗌 : `{settings["delete_flood_messages"]}`
"""
    )


# ─────────────────────────────
# SET FLOOD LIMIT
# ─────────────────────────────

@app.on_message(filters.command("setflood") & filters.group)
async def setflood(_, message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/setflood 5` or `/setflood off`"
        )

    arg = message.command[1].lower()

    if arg == "off":
        await set_flood_threshold(message.chat.id, 0)
        return await message.reply_text(
            "**🔴 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**"
        )

    threshold = int(arg)

    await set_flood_threshold(message.chat.id, threshold)

    await message.reply_text(
        f"**🛡️ Flood limit set to `{threshold}` messages.**"
    )


# ─────────────────────────────
# SET FLOOD MODE
# ─────────────────────────────

@app.on_message(filters.command("floodmode") & filters.group)
async def floodmode(_, message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/floodmode ban|mute|kick|tban|tmute`"
        )

    action = message.command[1].lower()

    if action not in ["ban", "mute", "kick", "tban", "tmute"]:
        return await message.reply_text(
            "**Invalid Action.**"
        )

    await set_flood_action(message.chat.id, action)

    await message.reply_text(
        f"**⚙️ Flood action set to `{action}`**"
    )


# ─────────────────────────────
# FLOOD DETECTION
# ─────────────────────────────

@app.on_message(filters.group & ~filters.service)
async def detect_flood(_, message):

    user = message.from_user
    chat_id = message.chat.id

    if not user:
        return

    if await is_admin(chat_id, user.id):
        return

    settings = await get_antiflood_settings(chat_id)

    if settings["flood_threshold"] == 0:
        return

    if user.id not in flood_tracker:
        flood_tracker[user.id] = {"count": 0, "messages": []}

    flood_tracker[user.id]["count"] += 1
    flood_tracker[user.id]["messages"].append(message)

    if flood_tracker[user.id]["count"] >= settings["flood_threshold"]:

        await take_action(message, settings)

        flood_tracker[user.id] = {"count": 0, "messages": []}


# ─────────────────────────────
# TAKE ACTION
# ─────────────────────────────

async def take_action(message, settings):

    chat_id = message.chat.id
    user_id = message.from_user.id
    action = settings["flood_action"]

    duration = await get_flood_action_duration(chat_id)

    if action == "ban":
        await app.ban_chat_member(chat_id, user_id)

    elif action == "kick":
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)

    elif action == "mute":
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions()
        )

    elif action == "tban":

        until = datetime.now() + timedelta(seconds=duration)

        await app.ban_chat_member(chat_id, user_id, until_date=until)

    elif action == "tmute":

        until = datetime.now() + timedelta(seconds=duration)

        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(),
            until_date=until
        )

    await message.reply_text(
        "**🚫 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝖳𝗋𝗂𝗀𝗀𝖾𝗋𝖾𝖽**\n"
        "> 𝖴𝗌𝖾𝗋 𝗐𝖺𝗌 𝗉𝗎𝗇𝗂𝗌𝗁𝖾𝖽 𝖿𝗈𝗋 𝗌𝗉𝖺𝗆𝗆𝗂𝗇𝗀."
    )

    if settings["delete_flood_messages"]:

        for msg in flood_tracker[user_id]["messages"]:
            try:
                await msg.delete()
            except:
                pass


# ─────────────────────────────

__MODULE__ = "𝖠𝗇𝗍𝗂𝖥𝗅𝗈𝗈𝖽"

__HELP__ = """
**🛡️ 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽**

/flood  
→ Show antiflood settings

/setflood <number/off>  
→ Set flood message limit

/floodmode ban|mute|kick|tban|tmute  
→ Set punishment mode
"""
