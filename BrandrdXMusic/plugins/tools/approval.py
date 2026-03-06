import asyncio
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatJoinRequest,
    InputMediaPhoto
)
from pyrogram import enums
from pyrogram.errors import FloodWait, RPCError

from BrandrdXMusic import app

LOG_CHANNEL_ID = -1003700186680
DEVELOPER_URL = "https://t.me/cyber_github"


# ===============================
# JOIN REQUEST HANDLER
# ===============================

@app.on_chat_join_request()
async def join_request_handler(client, request: ChatJoinRequest):

    user = request.from_user
    chat = request.chat

    try:
        username = f"@{user.username}" if user.username else "ɴ/ᴀ"
        first_name = user.first_name or "ɴ/ᴀ"
        last_name = user.last_name or "ɴ/ᴀ"
        is_bot = user.is_bot
        is_premium = getattr(user, "is_premium", False)

        # Try getting profile photo
        try:
            photos = await client.get_profile_photos(user.id, limit=1)
            user_photo = photos.photos[0][-1].file_id if photos.total > 0 else None
            photos_count = photos.total
        except:
            user_photo = None
            photos_count = 0

    except:
        username = first_name = last_name = "ɴ/ᴀ"
        is_bot = False
        is_premium = False
        photos_count = 0
        user_photo = None

    caption = (
        f"❖ ηєᴡ ᴊσɪη ʀєǫᴜєꜱᴛ\n\n"
        f"👤 ᴜꜱᴇʀ: {user.mention}\n"
        f"🆔 ɪᴅ: <code>{user.id}</code>\n"
        f"💬 ᴜsᴇʀɴᴀᴍᴇ: {username}\n"
        f"📝 ғɪʀsᴛ: {first_name}\n"
        f"📝 ʟᴀsᴛ: {last_name}\n"
        f"🤖 ʙᴏᴛ: {is_bot}\n"
        f"💎 ᴘʀᴇᴍɪᴜᴍ: {is_premium}\n"
        f"📸 ᴘɪᴄs: {photos_count}\n"
        f"🏷 ᴄʜᴀᴛ: {chat.title}\n\n"
        f"❖ ᴄʜσσsᴇ ᴀɴ ᴀᴄᴛɪᴏɴ:"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴀᴘᴘʀᴏᴠᴇ",
                    callback_data=f"approve|{chat.id}|{user.id}"
                ),
                InlineKeyboardButton(
                    "❌ ᴅᴇᴄʟɪɴᴇ",
                    callback_data=f"decline|{chat.id}|{user.id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "👀 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ",
                    url=f"tg://user?id={user.id}"
                )
            ]
        ]
    )

    try:
        if user_photo:
            await client.send_photo(
                chat.id,
                photo=user_photo,
                caption=caption,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await client.send_message(
                chat.id,
                caption,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)


# ===============================
# APPROVE / DECLINE BUTTONS
# ===============================

@app.on_callback_query(filters.regex("^(approve|decline)\|"))
async def join_request_buttons(client, callback):

    try:

        action, chat_id, user_id = callback.data.split("|")
        chat_id = int(chat_id)
        user_id = int(user_id)

        if action == "approve":
            await client.approve_chat_join_request(chat_id, user_id)
            result_text = (
                f"✅ ᴜꜱᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ\n\n"
                f"🆔 <code>{user_id}</code>"
            )
        else:
            await client.decline_chat_join_request(chat_id, user_id)
            result_text = (
                f"❌ ᴜꜱᴇʀ ᴅᴇᴄʟɪɴᴇᴅ\n\n"
                f"🆔 <code>{user_id}</code>"
            )

        try:
            if callback.message.photo:
                await callback.message.edit_media(
                    InputMediaPhoto(
                        callback.message.photo.file_id,
                        caption=result_text,
                        parse_mode=enums.ParseMode.HTML
                    )
                )
            else:
                await callback.message.edit_text(
                    result_text,
                    parse_mode=enums.ParseMode.HTML
                )
        except:
            pass

        await callback.answer()

        # LOG CHANNEL
        await client.send_message(
            LOG_CHANNEL_ID,
            result_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url=DEVELOPER_URL)]]
            ),
            parse_mode=enums.ParseMode.HTML
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except RPCError:
        pass

    except Exception:
        pass
