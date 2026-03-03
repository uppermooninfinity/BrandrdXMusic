import pytz
from datetime import datetime
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

# ================= STORAGE ================= #

nightmode_data = {}

DEFAULT_TZ = "Asia/Kolkata"

# ========================================== #

def sc(t: str):
    return t.lower()

async def is_admin(chat_id: int, user_id: int):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    )

# ================= COMMAND ================= #

@app.on_message(filters.command("nightmode", prefixes=["/"]) & filters.group)
async def nightmode_main(_, message: Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply(sc("only admins can use this 🚫"))

    chat_id = message.chat.id

    nightmode_data.setdefault(chat_id, {
        "enabled": False,
        "start": None,
        "end": None,
        "mode": "full",          # full / media / restrict
        "timezone": DEFAULT_TZ
    })

    data = nightmode_data[chat_id]

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌙 enable", callback_data="nm_enable"),
            InlineKeyboardButton("☀️ disable", callback_data="nm_disable")
        ],
        [InlineKeyboardButton("⏰ set time", callback_data="nm_settime")],
        [
            InlineKeyboardButton("🔒 full lock", callback_data="nm_mode_full"),
            InlineKeyboardButton("🗑 media only", callback_data="nm_mode_media")
        ],
        [InlineKeyboardButton("🔕 restrict mode", callback_data="nm_mode_restrict")],
        [InlineKeyboardButton("🌍 timezone", callback_data="nm_timezone")],
        [InlineKeyboardButton("❌ close", callback_data="nm_close")]
    ])

    await message.reply(
        sc(
            f"🌙 night mode panel\n\n"
            f"status: {'on' if data['enabled'] else 'off'}\n"
            f"time: {data['start']} → {data['end']}\n"
            f"mode: {data['mode']}\n"
            f"timezone: {data['timezone']}"
        ),
        reply_markup=buttons
    )

# ================= TIME GRID ================= #

def hour_keyboard(mode):
    rows = []
    row = []
    for i in range(24):
        row.append(
            InlineKeyboardButton(str(i), callback_data=f"nm_hour_{mode}_{i}")
        )
        if len(row) == 6:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("⬅ back", callback_data="nm_back")])
    return InlineKeyboardMarkup(rows)

@app.on_callback_query(filters.regex("^nm_settime$"))
async def nm_settime(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    await query.message.edit_text(
        sc("👉 select starting hour (0-23)"),
        reply_markup=hour_keyboard("start")
    )

@app.on_callback_query(filters.regex("^nm_hour_"))
async def nm_hour(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    chat_id = query.message.chat.id
    _, _, mode, hour = query.data.split("_")
    hour = int(hour)

    if mode == "start":
        nightmode_data[chat_id]["start"] = hour
        await query.message.edit_text(
            sc("👉 select ending hour (0-23)"),
            reply_markup=hour_keyboard("end")
        )
    else:
        nightmode_data[chat_id]["end"] = hour
        await query.message.edit_text(
            sc(f"✅ night time set {nightmode_data[chat_id]['start']} → {hour}")
        )

# ================= ENABLE / DISABLE ================= #

@app.on_callback_query(filters.regex("^nm_enable$"))
async def nm_enable(_, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    nightmode_data[query.message.chat.id]["enabled"] = True
    await query.answer("night mode enabled 🌙")

@app.on_callback_query(filters.regex("^nm_disable$"))
async def nm_disable(_, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    nightmode_data[query.message.chat.id]["enabled"] = False
    await query.answer("night mode disabled ☀️")

# ================= MODE SELECT ================= #

@app.on_callback_query(filters.regex("^nm_mode_"))
async def nm_mode(_, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    mode = query.data.split("_")[2]
    nightmode_data[query.message.chat.id]["mode"] = mode
    await query.answer(f"mode set: {mode}")

# ================= TIMEZONE ================= #

@app.on_callback_query(filters.regex("^nm_timezone$"))
async def nm_timezone(_, query: CallbackQuery):

    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Asia/Kolkata", callback_data="nm_tz_Asia/Kolkata")],
        [InlineKeyboardButton("UTC", callback_data="nm_tz_UTC")],
        [InlineKeyboardButton("Europe/London", callback_data="nm_tz_Europe/London")],
        [InlineKeyboardButton("⬅ back", callback_data="nm_back")]
    ])

    await query.message.edit_text(
        sc("🌍 select timezone"),
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^nm_tz_"))
async def nm_tz_set(_, query: CallbackQuery):
    tz = query.data.replace("nm_tz_", "")
    nightmode_data[query.message.chat.id]["timezone"] = tz
    await query.answer("timezone updated 🌍")

# ================= BACK / CLOSE ================= #

@app.on_callback_query(filters.regex("^nm_back$"))
async def nm_back(_, query: CallbackQuery):
    await nightmode_main(_, query.message)

@app.on_callback_query(filters.regex("^nm_close$"))
async def nm_close(_, query: CallbackQuery):
    await query.message.delete()

# ================= NIGHT CHECK ================= #

def is_night(chat_id):
    data = nightmode_data.get(chat_id)
    if not data or not data["enabled"]:
        return False

    tz = pytz.timezone(data["timezone"])
    now = datetime.now(tz).hour
    start = data["start"]
    end = data["end"]

    if start is None or end is None:
        return False

    if start < end:
        return start <= now < end
    else:
        return now >= start or now < end

# ================= ENFORCER ================= #

@app.on_message(filters.group & ~filters.service)
async def night_enforcer(_, message: Message):

    chat_id = message.chat.id

    if not is_night(chat_id):
        return

    if not message.from_user:
        return

    member = await app.get_chat_member(chat_id, message.from_user.id)

    if member.status in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ):
        return

    mode = nightmode_data[chat_id]["mode"]

    try:
        if mode == "full":
            await message.delete()

        elif mode == "media":
            if (
                message.photo or message.video or message.sticker or
                message.animation or message.document or message.voice
            ):
                await message.delete()

        elif mode == "restrict":
            await app.restrict_chat_member(
                chat_id,
                message.from_user.id,
                ChatPermissions()
            )
    except:
        pass
