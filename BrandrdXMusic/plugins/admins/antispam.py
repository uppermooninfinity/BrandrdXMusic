import time
import asyncio
from collections import defaultdict
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions
)
from pyrogram.enums import ChatMemberStatus

from BrandrdXMusic import app

# ================= CONFIG ================= #

SPAM_LIMIT = 5
AUTO_DELETE_TIME = 15

DEVELOPER_URL = "https://t.me/cyber_github"

chat_settings = {}
user_messages = defaultdict(list)

# ========================================== #

def sc(text: str):
    return text.lower()

async def is_admin(chat_id: int, user_id: int):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    )

# ================= COMMAND ================= #

@app.on_message(filters.command("antispam") & filters.group)
async def antispam_panel(_, message: Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply(
            "<blockquote>⛔ ᴀᴅᴍɪɴs ᴏɴʟʏ</blockquote>",
            quote=True
        )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ sᴇᴛ ᴛɪᴍᴇ", callback_data="spam_time")],
        [
            InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ", callback_data="act_delete"),
            InlineKeyboardButton("⚠️ ᴡᴀʀɴ", callback_data="act_warn"),
        ],
        [
            InlineKeyboardButton("🔇 ᴍᴜᴛᴇ", callback_data="act_mute"),
            InlineKeyboardButton("👢 ᴋɪᴄᴋ", callback_data="act_kick"),
        ],
        [
            InlineKeyboardButton("🚫 ʙᴀɴ", callback_data="act_ban"),
        ],
        [
            InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")
        ]
    ])

    await message.reply(
        """
<blockquote>⚔️ ᴀɴᴛɪ-sᴘᴀᴍ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ</blockquote>

<blockquote>
“ᴀ ᴄʟᴇᴀɴ ᴄʜᴀᴛ ɪs ᴀ ʜᴀᴘᴘʏ ᴄʜᴀᴛ.”
</blockquote>

<blockquote>
“sᴘᴀᴍ ᴅᴇsᴛʀᴏʏs ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs,
ʀᴇsᴘᴇᴄᴛ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ.”
</blockquote>

⚙ sᴇᴛ ᴛɪᴍᴇ ᴀɴᴅ ᴀᴄᴛɪᴏɴ ʙᴇʟᴏᴡ
""",
        reply_markup=buttons,
        quote=True
    )

# ================= TIME SELECT ================= #

@app.on_callback_query(filters.regex("^spam_time$"))
async def select_time(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("2s", callback_data="set_2"),
            InlineKeyboardButton("3s", callback_data="set_3"),
            InlineKeyboardButton("5s", callback_data="set_5"),
            InlineKeyboardButton("10s", callback_data="set_10"),
        ],
        [
            InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")
        ]
    ])

    await query.message.edit_text(
        "<blockquote>⏱ sᴇʟᴇᴄᴛ ᴛɪᴍᴇ ɪɴᴛᴇʀᴠᴀʟ</blockquote>",
        reply_markup=buttons
    )

# ================= SET TIME ================= #

@app.on_callback_query(filters.regex("^set_"))
async def set_time(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    seconds = int(query.data.split("_")[1])

    chat_settings.setdefault(query.message.chat.id, {})
    chat_settings[query.message.chat.id]["time"] = seconds

    await query.answer("time set ✓")

# ================= SET ACTION ================= #

@app.on_callback_query(filters.regex("^act_"))
async def set_action(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    action = query.data.split("_")[1]

    chat_settings.setdefault(query.message.chat.id, {})
    chat_settings[query.message.chat.id]["action"] = action

    await query.answer(f"action set: {action}")

# ================= CLOSE ================= #

@app.on_callback_query(filters.regex("^close$"))
async def close_btn(_, query: CallbackQuery):
    await query.message.delete()

# ================= SPAM DETECTOR ================= #

@app.on_message(filters.group & ~filters.service)
async def detect_spam(_, message: Message):

    chat_id = message.chat.id

    if chat_id not in chat_settings:
        return

    settings = chat_settings[chat_id]

    if "time" not in settings or "action" not in settings:
        return

    if not message.from_user:
        return

    user_id = message.from_user.id
    now = time.time()

    interval = settings["time"]
    action = settings["action"]

    user_messages[(chat_id, user_id)] = [
        t for t in user_messages[(chat_id, user_id)]
        if now - t < interval
    ]

    user_messages[(chat_id, user_id)].append(now)

    if len(user_messages[(chat_id, user_id)]) >= SPAM_LIMIT:

        try:
            await message.delete()
        except:
            pass

        # ===== ACTIONS ===== #

        if action == "mute":
            await app.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions()
            )

        elif action == "kick":
            await app.ban_chat_member(chat_id, user_id)
            await app.unban_chat_member(chat_id, user_id)

        elif action == "ban":
            await app.ban_chat_member(chat_id, user_id)

        # ===== WARNING MESSAGE ===== #

        warn = await app.send_message(
            chat_id,
            f"""
<blockquote>⚠️ sᴘᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ</blockquote>

👤 {message.from_user.mention}

⚡ {SPAM_LIMIT} ᴍᴇssᴀɢᴇs ɪɴ {interval}s  
🛡 ᴀᴄᴛɪᴏɴ : {action}

<blockquote>
“ʀᴇsᴘᴇᴄᴛ ᴛʜᴇ ᴄʜᴀᴛ,
ᴏʀ ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ.”
</blockquote>

<blockquote>
“ɢᴏᴏᴅ ᴄᴏᴍᴍᴜɴɪᴛɪᴇs
ᴀʀᴇ ʙᴜɪʟᴛ ᴏɴ ʀᴇsᴘᴇᴄᴛ.”
</blockquote>
"""
        )

        await asyncio.sleep(AUTO_DELETE_TIME)

        try:
            await warn.delete()
        except:
            pass

        user_messages[(chat_id, user_id)] = []
