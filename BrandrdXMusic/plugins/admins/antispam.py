import time
from collections import defaultdict
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from BrandrdXMusic import app  # IMPORTANT

# ================= SETTINGS ================= #

DEVELOPER_URL = "https://t.me/cyber_github"
SPAM_LIMIT = 5

chat_settings = {}
user_messages = defaultdict(list)

# ============================================ #

def sc(text: str):
    return text.lower()

async def is_admin(chat_id: int, user_id: int):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")

# ================= COMMAND =================== #

@app.on_message(filters.command("antispam", prefixes=["/"]) & filters.group)
async def antispam_panel(_, message: Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply(sc("only admins can use this 🚫🔥"))

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ ᴛɪᴍᴇ", callback_data="spam_time")],
        [InlineKeyboardButton("❌ ᴏғғ", callback_data="spam_off")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]
    ])

    await message.reply(
        sc("⚔️ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ 🔥"),
        reply_markup=buttons
    )

# ================= TIME SELECT ================= #

@app.on_callback_query(filters.regex("^spam_time$"))
async def time_selector(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only 🚫", show_alert=True)

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("2s", callback_data="set_2"),
            InlineKeyboardButton("3s", callback_data="set_3"),
            InlineKeyboardButton("5s", callback_data="set_5"),
            InlineKeyboardButton("10s", callback_data="set_10"),
        ],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]
    ])

    await query.message.edit_text(
        sc("⏱ select time interval 🔥"),
        reply_markup=buttons
    )

# ================= SET TIME ================= #

@app.on_callback_query(filters.regex("^set_"))
async def set_time(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only 🚫", show_alert=True)

    seconds = int(query.data.split("_")[1])
    chat_settings[query.message.chat.id] = seconds

    await query.message.edit_text(
        sc(
            f"🔥 antispam active\n\n"
            f"📨 limit: {SPAM_LIMIT} messages\n"
            f"⏱ time: {seconds}s"
        )
    )

# ================= TURN OFF ================= #

@app.on_callback_query(filters.regex("^spam_off$"))
async def spam_off(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only 🚫", show_alert=True)

    chat_settings.pop(query.message.chat.id, None)
    await query.message.edit_text(sc("❌ antispam disabled"))

# ================= CLOSE ================= #

@app.on_callback_query(filters.regex("^close$"))
async def close_btn(_, query: CallbackQuery):
    await query.message.delete()

# ================= BAN BUTTON ================= #

@app.on_callback_query(filters.regex("^ban_"))
async def ban_user(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only 🚫", show_alert=True)

    user_id = int(query.data.split("_")[1])
    await app.ban_chat_member(query.message.chat.id, user_id)

    await query.message.edit_text(sc("🚫 user banned ⚔️"))

# ================= SPAM DETECTOR ================= #

@app.on_message(filters.group & ~filters.service)
async def detect_spam(_, message: Message):

    chat_id = message.chat.id

    if chat_id not in chat_settings:
        return

    if not message.from_user:
        return

    user_id = message.from_user.id
    now = time.time()
    interval = chat_settings[chat_id]

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

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚫 ʙᴀɴ", callback_data=f"ban_{user_id}")],
            [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=DEVELOPER_URL)],
            [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]
        ])

        await app.send_message(
            chat_id,
            sc(
                f"⚠️ spam detected 🔥\n\n"
                f"👤 {message.from_user.mention}\n"
                f"📨 {SPAM_LIMIT} messages in {interval}s\n\n"
                f"@admins please overlook ⚔️"
            ),
            reply_markup=buttons
        )

        user_messages[(chat_id, user_id)] = []
