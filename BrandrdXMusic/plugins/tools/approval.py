from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatJoinRequest
)
from BrandrdXMusic import app

LOG_CHANNEL_ID = -1003700186680
DEVELOPER_URL = "https://t.me/cyber_github"


# ===============================
# 🔔 JOIN REQUEST HANDLER
# ===============================

@app.on_chat_join_request()
async def join_request_handler(client, request: ChatJoinRequest):

    user = request.from_user
    chat = request.chat

    try:
        full_user = await client.get_users(user.id)
        username = f"@{full_user.username}" if full_user.username else "ɴ/ᴀ"
        first_name = full_user.first_name or "ɴ/ᴀ"
        last_name = full_user.last_name or "ɴ/ᴀ"
        is_bot = full_user.is_bot
        is_premium = getattr(full_user, "is_premium", False)
        dc_id = getattr(full_user, "dc_id", "ɴ/ᴀ")

        profile_photos = await client.get_profile_photos(user.id)
        photos_count = profile_photos.total if profile_photos else 0
        user_photo = profile_photos.photos[0][-1].file_id if photos_count > 0 else None

    except:
        username = first_name = last_name = "ɴ/ᴀ"
        is_bot = False
        is_premium = False
        dc_id = "ɴ/ᴀ"
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
        f"🌍 ᴅᴄ ɪᴅ: {dc_id}\n"
        f"📸 ᴘɪᴄs: {photos_count}\n"
        f"🏷 ᴄʜᴀᴛ: {chat.title}\n\n"
        f"❖ ᴄʜσσsᴇ ᴀɴ ᴀᴄᴛɪᴏɴ:"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴀᴘᴘʀᴏᴠᴇ",
                    callback_data=f"approve_{chat.id}_{user.id}"
                ),
                InlineKeyboardButton(
                    "❌ ᴅᴇᴄʟɪɴᴇ",
                    callback_data=f"decline_{chat.id}_{user.id}"
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

    if user_photo:
        await client.send_photo(
            chat.id,
            photo=user_photo,
            caption=caption,
            reply_markup=buttons,
            parse_mode="HTML"
        )
    else:
        await client.send_message(
            chat.id,
            caption,
            reply_markup=buttons,
            parse_mode="HTML"
        )


# ===============================
# 🔘 APPROVE / DECLINE
# ===============================

@app.on_callback_query(filters.regex("^(approve_|decline_)"))
async def join_request_buttons(client, callback):

    await callback.answer()

    data = callback.data.split("_")
    action = data[0]
    chat_id = int(data[1])
    user_id = int(data[2])

    try:
        profile_photos = await client.get_profile_photos(user_id)
        photos_count = profile_photos.total if profile_photos else 0
        user_photo = profile_photos.photos[0][-1].file_id if photos_count > 0 else None
    except:
        user_photo = None

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
        if user_photo:
            await callback.message.edit_media(
                media=callback.message.photo.file_id
            )
            await callback.message.edit_caption(result_text, parse_mode="html")
        else:
            await callback.message.edit_text(result_text, parse_mode="html")
    except:
        pass

    # LOG CHANNEL
    await client.send_message(
        LOG_CHANNEL_ID,
        result_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url=DEVELOPER_URL)]]
        ),
        parse_mode="HTML"
    )
