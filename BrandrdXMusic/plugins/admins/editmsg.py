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
PING_VID_URL = "https://files.catbox.moe/nfofiu.gif"

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


# ================= CONTROL PANEL =================

@app.on_message(filters.command("editmsg") & filters.group)
async def editmsg_panel(client, message):

    if not message.from_user:
        return

    try:
        member = await app.get_chat_member(message.chat.id, message.from_user.id)

        if not member.privileges or not member.privileges.can_delete_messages:
            return await message.reply("› ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.")

        status = await get_edit_status(message.chat.id)
        state = "ᴇɴᴀʙʟᴇᴅ ✅" if status else "ᴅɪsᴀʙʟᴇᴅ ❌"

        text = (
            "⚙️ ᴇᴅɪᴛ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴘᴀɴᴇʟ\n\n"
            f"❖ sᴛᴀᴛᴜs : {state}\n\n"
            "ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ 👇"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🟢 ᴏɴ", callback_data="edit_on"),
                    InlineKeyboardButton("🔴 ᴏғғ", callback_data="edit_off"),
                ],
                [
                    InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="edit_close")
                ]
            ]
        )

        await message.reply_video(
            video=PING_VID_URL,
            caption=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )

    except Exception:
        pass


# ================= BUTTON HANDLER =================

@app.on_callback_query(filters.regex("^edit_"))
async def edit_buttons(client, callback):

    try:

        chat_id = callback.message.chat.id
        user_id = callback.from_user.id

        member = await app.get_chat_member(chat_id, user_id)

        if not member.privileges or not member.privileges.can_delete_messages:
            return await callback.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.", show_alert=True)

        if callback.data == "edit_on":
            await set_edit_status(chat_id, True)
            await callback.answer("ᴇɴᴀʙʟᴇᴅ")

        elif callback.data == "edit_off":
            await set_edit_status(chat_id, False)
            await callback.answer("ᴅɪsᴀʙʟᴇᴅ")

        elif callback.data == "edit_close":
            return await callback.message.delete()

        status = await get_edit_status(chat_id)
        state = "ᴇɴᴀʙʟᴇᴅ ✅" if status else "ᴅɪsᴀʙʟᴇᴅ ❌"

        await callback.message.edit_caption(
            caption=f"⚙️ ᴇᴅɪᴛ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ\n\n❖ sᴛᴀᴛᴜs : {state}",
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception:
        pass


# ================= CLOSE BUTTON =================

@app.on_callback_query(filters.regex("clone"))
async def close_warn(client, callback):
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

        # ignore reactions / service edits
        if not message.text and not message.caption:
            return

        member = await app.get_chat_member(message.chat.id, message.from_user.id)

        # ignore admins
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

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        group_text = (
            f"❖ ʜᴇʏ , {username}\n"
            "๏ ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ !!\n\n"
            "❖ ᴄᴏɴᴛʀᴏʟ : /editmsg"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", user_id=OWNER_ID),
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="clone")
                ]
            ]
        )

        warn = await app.send_video(
            chat_id,
            video=PING_VID_URL,
            caption=group_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )

        await asyncio.sleep(8)

        try:
            await warn.delete()
        except:
            pass

        # ================= LOG =================

        edited_content = message.text or message.caption

        log_text = (
            "📝 ᴇᴅɪᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n"
            f"❖ ᴄʜᴀᴛ : {chat_title}\n"
            f"❖ ᴄʜᴀᴛ ɪᴅ : `{chat_id}`\n"
            f"❖ ᴜsᴇʀ : {username}\n"
            f"❖ ᴜsᴇʀ ɪᴅ : `{user_id}`\n"
            f"❖ ᴛɪᴍᴇ : `{timestamp}`\n\n"
            f"`{edited_content}`"
        )

        await app.send_video(
            FED_LOG_CHANNEL,
            video=PING_VID_URL,
            caption=log_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Developer", user_id=OWNER_ID)]]
            )
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except RPCError:
        pass

    except Exception:
        pass
