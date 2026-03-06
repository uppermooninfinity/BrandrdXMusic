import asyncio
from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, RPCError

from BrandrdXMusic import app
from BrandrdXMusic.utils.mongo import db

# ================= CONFIG =================

FED_LOG_CHANNEL = -1003700186680
OWNER_ID = 7651303468

EDIT_COLL = db.edit_settings


# ================= DATABASE =================

async def set_edit_status(chat_id: int, status: bool):
    try:
        await EDIT_COLL.update_one(
            {"chat_id": chat_id},
            {"$set": {"enabled": status}},
            upsert=True
        )
    except:
        pass


async def get_edit_status(chat_id: int):
    try:
        data = await EDIT_COLL.find_one({"chat_id": chat_id})
        return data.get("enabled", False) if data else False
    except:
        return False


# ================= PANEL =================

@app.on_message(filters.command("editmsg") & filters.group)
async def editmsg_panel(client, message):

    if not message.from_user:
        return

    try:
        member = await app.get_chat_member(message.chat.id, message.from_user.id)

        if not member.privileges or not member.privileges.can_delete_messages:
            return await message.reply("❌ ᴀᴅᴍɪɴ ᴏɴʟʏ")

        status = await get_edit_status(message.chat.id)
        state = "ᴏɴ ✅" if status else "ᴏғғ ❌"

        text = (
            "⚙️ ᴇᴅɪᴛ ᴘʀᴏᴛᴇᴄᴛ\n\n"
            f"ꜱᴛᴀᴛᴜꜱ : {state}"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🟢 ᴏɴ", callback_data="edit_on"),
                    InlineKeyboardButton("🔴 ᴏғғ", callback_data="edit_off"),
                ],
                [
                    InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")
                ]
            ]
        )

        await message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )

    except:
        pass


# ================= BUTTONS =================

@app.on_callback_query(filters.regex("^edit_"))
async def edit_buttons(client, callback):

    try:

        chat_id = callback.message.chat.id
        user_id = callback.from_user.id

        member = await app.get_chat_member(chat_id, user_id)

        if not member.privileges or not member.privileges.can_delete_messages:
            return await callback.answer("❌ admin only", show_alert=True)

        if callback.data == "edit_on":
            await set_edit_status(chat_id, True)
            await callback.answer("enabled")

        elif callback.data == "edit_off":
            await set_edit_status(chat_id, False)
            await callback.answer("disabled")

        status = await get_edit_status(chat_id)
        state = "ᴏɴ ✅" if status else "ᴏғғ ❌"

        await callback.message.edit_text(
            f"⚙️ ᴇᴅɪᴛ ᴘʀᴏᴛᴇᴄᴛ\n\nꜱᴛᴀᴛᴜꜱ : {state}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🟢 ᴏɴ", callback_data="edit_on"),
                        InlineKeyboardButton("🔴 ᴏғғ", callback_data="edit_off"),
                    ],
                    [
                        InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ]
            )
        )

    except:
        pass


# ================= CLOSE =================

@app.on_callback_query(filters.regex("^close$"))
async def close_panel(client, callback):
    try:
        await callback.message.delete()
    except:
        pass


# ================= EDIT DETECTION =================

@app.on_edited_message(filters.group)
async def detect_edit(client, message):

    try:

        if not message.from_user:
            return

        enabled = await get_edit_status(message.chat.id)

        if not enabled:
            return

        # ignore reactions / non text edits
        if not message.text and not message.caption:
            return

        member = await app.get_chat_member(message.chat.id, message.from_user.id)

        if member.status in ["administrator", "creator"]:
            return

        try:
            await message.delete()
        except:
            return

        username = message.from_user.mention
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_title = message.chat.title or "Unknown"

        timestamp = datetime.utcnow().strftime("%H:%M:%S")

        warn = await app.send_message(
            chat_id,
            f"⚠️ {username} edited message\n"
            "editing not allowed"
        )

        await asyncio.sleep(3)

        try:
            await warn.delete()
        except:
            pass

        # ================= LOG =================

        edited_content = message.text or message.caption

        log_text = (
            "📝 edit removed\n\n"
            f"chat : {chat_title}\n"
            f"user : {username}\n"
            f"id : `{user_id}`\n"
            f"time : `{timestamp}`\n\n"
            f"`{edited_content}`"
        )

        await app.send_message(
            FED_LOG_CHANNEL,
            log_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Developer", user_id=OWNER_ID)]]
            )
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except RPCError:
        pass

    except:
        pass
