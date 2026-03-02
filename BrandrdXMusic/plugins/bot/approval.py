from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatJoinRequest
)
from BrandrdXMusic import app

# ===============================
# CONFIG
# ===============================

LOG_CHANNEL_ID = -1001234567890  # 🔴 PUT YOUR LOG CHANNEL ID
DEVELOPER_URL = "https://t.me/yourusername"  # 🔴 PUT YOUR USERNAME

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
        profile_photos = await client.get_profile_photos(user.id)
        photos_count = profile_photos.total if profile_photos else 0
        user_photo = profile_photos.photos[0][-1].file_id if photos_count > 0 else None
    except Exception:
        username = first_name = last_name = "ɴ/ᴀ"
        is_bot = False
        photos_count = 0
        user_photo = None

    caption_text = (
        f"❖ ηєᴡ ᴊσɪη ʀєǫᴜєꜱᴛ\n\n"
        f"👤 ᴜꜱᴇʀ: {user.mention}\n"
        f"🆔 ɪᴅ: `{user.id}`\n"
        f"💬 ᴜsᴇʀɴᴀᴍᴇ: {username}\n"
        f"📝 ғɪʀsᴛ ɴᴀᴍᴇ: {first_name}\n"
        f"📝 ʟᴀsᴛ ɴᴀᴍᴇ: {last_name}\n"
        f"🤖 ʙᴏᴛ: {is_bot}\n"
        f"📸 ᴘʀᴏғɪʟᴇ ᴘɪᴄs: {photos_count}\n"
        f"🏷 ᴄʜᴀᴛ: {chat.title}\n"
        f"🆔 ᴄʜᴀᴛ ɪᴅ: `{chat.id}`\n\n"
        f"❖ ᴄʜσσsᴇ ᴀɴ ᴀᴄᴛɪᴏɴ ʙᴇʟᴏᴡ:"
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

    # ================= SEND TO GROUP =================

    if user_photo:
        await client.send_photo(
            chat_id=chat.id,
            photo=user_photo,
            caption=caption_text,
            reply_markup=buttons,
            parse_mode="html"
        )
    else:
        await client.send_message(
            chat_id=chat.id,
            text=caption_text,
            reply_markup=buttons,
            parse_mode="html"
        )

    # ================= LOG CHANNEL =================

    log_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👀 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ",
                    url=f"tg://user?id={user.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                    url=DEVELOPER_URL
                )
            ]
        ]
    )

    if user_photo:
        await client.send_photo(
            chat_id=LOG_CHANNEL_ID,
            photo=user_photo,
            caption=caption_text,
            reply_markup=log_buttons,
            parse_mode="html"
        )
    else:
        await client.send_message(
            chat_id=LOG_CHANNEL_ID,
            text=caption_text,
            reply_markup=log_buttons,
            parse_mode="html"
        )


# ===============================
# 🔘 APPROVE / DECLINE HANDLER
# ===============================

@app.on_callback_query(filters.regex("approve_|decline_"))
async def join_request_buttons(client, callback):

    data = callback.data.split("_")
    action = data[0]
    chat_id = int(data[1])
    user_id = int(data[2])

    try:
        if action == "approve":
            await client.approve_chat_join_request(chat_id, user_id)

            await callback.message.edit_caption(
                "✅ ᴜꜱᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ."
            )

            await client.send_message(
                LOG_CHANNEL_ID,
                f"✅ ᴜꜱᴇʀ `{user_id}` ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ `{chat_id}`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                                url=DEVELOPER_URL
                            )
                        ]
                    ]
                )
            )

        elif action == "decline":
            await client.decline_chat_join_request(chat_id, user_id)

            await callback.message.edit_caption(
                "❌ ᴜꜱᴇʀ ᴅᴇᴄʟɪɴᴇᴅ."
            )

            await client.send_message(
                LOG_CHANNEL_ID,
                f"❌ ᴜꜱᴇʀ `{user_id}` ᴅᴇᴄʟɪɴᴇᴅ ɪɴ `{chat_id}`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                                url=DEVELOPER_URL
                            )
                        ]
                    ]
                )
            )

        await callback.answer("ᴅᴏɴᴇ")

    except Exception as e:
        await callback.answer(f"ᴇʀʀᴏʀ: {e}", show_alert=True)
