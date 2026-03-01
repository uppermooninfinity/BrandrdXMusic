from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatJoinRequest
)
from BrandrdXMusic import app

# ===============================
# 🔔 Detect Join Request with Video
# ===============================

@app.on_chat_join_request()
async def join_request_handler(client, request: ChatJoinRequest):

    user = request.from_user
    chat = request.chat

    # Fetch more user info
    try:
        full_user = await client.get_users(user.id)
        username = f"@{full_user.username}" if full_user.username else "N/A"
        first_name = full_user.first_name or "N/A"
        last_name = full_user.last_name or "N/A"
        is_bot = full_user.is_bot
        profile_photos = await client.get_profile_photos(user.id)
        photos_count = profile_photos.total if profile_photos else 0
    except Exception:
        username = first_name = last_name = "N/A"
        is_bot = False
        photos_count = 0

    # Inline buttons with custom font
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

    # Send the video with user info in caption (custom font)
    caption_text = (
        f"❖ ηєᴡ ᴊσɪη ʀєǫᴜєꜱᴛ ✨\n\n"
        f"👤 ᴜꜱєʀ: {user.mention}\n"
        f"🆔 ɪᴅ: `{user.id}`\n"
        f"💬 ᴜsєʀɴᴀᴍє: {username}\n"
        f"📝 ғɪʀsᴛ ɴᴀᴍє: {first_name}\n"
        f"📝 ʟᴀsᴛ ɴᴀᴍє: {last_name}\n"
        f"🤖 ʙᴏᴛ: {is_bot}\n"
        f"📸 ᴘʀᴏғɪʟє ᴘɪᴄs: {photos_count}\n\n"
        f"❖ ᴄʜσσsє ᴀɴ ᴀᴄᴛɪᴏɴ ʙᴇʟᴏᴡ:"
    )

    await client.send_video(
        chat_id=chat.id,
        video="https://example.com/sample.mp4",  # Replace with your video URL or file_id
        caption=caption_text,
        reply_markup=buttons,
        parse_mode="html"
    )


# ===============================
# 🔘 Button Handler
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
            await callback.message.edit_text("✅ ᴜsєʀ ᴀᴘᴘʀᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")

        elif action == "decline":
            await client.decline_chat_join_request(chat_id, user_id)
            await callback.message.edit_text("❌ ᴜsєʀ ᴅᴇᴄʟɪɴᴇᴅ.")

    except Exception as e:
        await callback.answer(f"Error: {e}", show_alert=True)
