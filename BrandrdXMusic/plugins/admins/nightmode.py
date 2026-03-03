import pytz
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions
)
from pyrogram.enums import ChatMemberStatus

# ================= MEMORY STORAGE =================

nightmode_data = {}
DEFAULT_TZ = "Asia/Kolkata"

# ==================================================


async def is_admin(client: Client, chat_id: int, user_id: int):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
        )
    except:
        return False


# ================= MAIN PANEL =================

@Client.on_message(filters.command("nightmode", prefixes=["/"]) & filters.group)
async def nightmode_panel(client: Client, message: Message):

    if not message.from_user:
        return

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("only admins can use this.")

    chat_id = message.chat.id

    nightmode_data.setdefault(chat_id, {
        "enabled": False,
        "start": None,
        "end": None,
        "mode": "full",  # full / media / restrict
        "timezone": DEFAULT_TZ
    })

    data = nightmode_data[chat_id]

    text = (
        "🌙 night mode panel\n\n"
        f"status: {'enabled' if data['enabled'] else 'disabled'}\n"
        f"time: {data['start']} → {data['end']}\n"
        f"mode: {data['mode']}\n"
        f"timezone: {data['timezone']}"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("enable 🌙", callback_data="nm_enable"),
            InlineKeyboardButton("disable ☀️", callback_data="nm_disable")
        ],
        [InlineKeyboardButton("set time ⏰", callback_data="nm_settime")],
        [
            InlineKeyboardButton("full lock 🔒", callback_data="nm_mode_full"),
            InlineKeyboardButton("media only 🗑", callback_data="nm_mode_media")
        ],
        [InlineKeyboardButton("restrict mode 🔕", callback_data="nm_mode_restrict")],
        [InlineKeyboardButton("timezone 🌍", callback_data="nm_timezone")],
        [InlineKeyboardButton("close ❌", callback_data="nm_close")]
    ])

    await message.reply_text(text, reply_markup=buttons)


# ================= TIME GRID =================

def hour_keyboard(mode: str):
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

    rows.append([InlineKeyboardButton("back ⬅", callback_data="nm_back")])
    return InlineKeyboardMarkup(rows)


@Client.on_callback_query(filters.regex("^nm_settime$"))
async def set_time(client: Client, query: CallbackQuery):

    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    await query.message.edit_text(
        "select start hour (0-23)",
        reply_markup=hour_keyboard("start")
    )


@Client.on_callback_query(filters.regex("^nm_hour_"))
async def select_hour(client: Client, query: CallbackQuery):

    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    chat_id = query.message.chat.id
    _, _, mode, hour = query.data.split("_")
    hour = int(hour)

    if mode == "start":
        nightmode_data[chat_id]["start"] = hour
        await query.message.edit_text(
            "select end hour (0-23)",
            reply_markup=hour_keyboard("end")
        )
    else:
        nightmode_data[chat_id]["end"] = hour
        await query.message.edit_text(
            f"time set: {nightmode_data[chat_id]['start']} → {hour}"
        )


# ================= ENABLE / DISABLE =================

@Client.on_callback_query(filters.regex("^nm_enable$"))
async def enable_nm(client: Client, query: CallbackQuery):
    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    nightmode_data[query.message.chat.id]["enabled"] = True
    await query.answer("night mode enabled")


@Client.on_callback_query(filters.regex("^nm_disable$"))
async def disable_nm(client: Client, query: CallbackQuery):
    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    nightmode_data[query.message.chat.id]["enabled"] = False
    await query.answer("night mode disabled")


# ================= MODE SELECT =================

@Client.on_callback_query(filters.regex("^nm_mode_"))
async def set_mode(client: Client, query: CallbackQuery):
    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    mode = query.data.split("_")[2]
    nightmode_data[query.message.chat.id]["mode"] = mode
    await query.answer(f"mode set: {mode}")


# ================= TIMEZONE =================

@Client.on_callback_query(filters.regex("^nm_timezone$"))
async def timezone_panel(client: Client, query: CallbackQuery):

    if not await is_admin(client, query.message.chat.id, query.from_user.id):
        return await query.answer("admins only", show_alert=True)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Asia/Kolkata", callback_data="nm_tz_Asia/Kolkata")],
        [InlineKeyboardButton("UTC", callback_data="nm_tz_UTC")],
        [InlineKeyboardButton("Europe/London", callback_data="nm_tz_Europe/London")],
        [InlineKeyboardButton("back ⬅", callback_data="nm_back")]
    ])

    await query.message.edit_text("select timezone", reply_markup=buttons)


@Client.on_callback_query(filters.regex("^nm_tz_"))
async def set_timezone(client: Client, query: CallbackQuery):
    tz = query.data.replace("nm_tz_", "")
    nightmode_data[query.message.chat.id]["timezone"] = tz
    await query.answer("timezone updated")


# ================= BACK / CLOSE =================

@Client.on_callback_query(filters.regex("^nm_back$"))
async def back_panel(client: Client, query: CallbackQuery):
    await nightmode_panel(client, query.message)


@Client.on_callback_query(filters.regex("^nm_close$"))
async def close_panel(_, query: CallbackQuery):
    await query.message.delete()


# ================= NIGHT CHECK =================

def is_night(chat_id):
    data = nightmode_data.get(chat_id)
    if not data or not data["enabled"]:
        return False

    if data["start"] is None or data["end"] is None:
        return False

    tz = pytz.timezone(data["timezone"])
    now_hour = datetime.now(tz).hour
    start = data["start"]
    end = data["end"]

    if start < end:
        return start <= now_hour < end
    else:
        return now_hour >= start or now_hour < end


# ================= ENFORCER =================

@Client.on_message(filters.group & ~filters.service)
async def enforce_nightmode(client: Client, message: Message):

    chat_id = message.chat.id

    if not is_night(chat_id):
        return

    if not message.from_user:
        return

    if await is_admin(client, chat_id, message.from_user.id):
        return

    mode = nightmode_data[chat_id]["mode"]

    try:
        if mode == "full":
            await message.delete()

        elif mode == "media":
            if (
                message.photo or message.video or message.sticker or
                message.animation or message.document or
                message.voice or message.video_note
            ):
                await message.delete()

        elif mode == "restrict":
            await client.restrict_chat_member(
                chat_id,
                message.from_user.id,
                ChatPermissions()
            )
    except:
        pass
