import asyncio
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatJoinRequest
)
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait

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

    username = f"@{user.username}" if user.username else "No Username"

    caption = (
        f"✨ **New Join Request**\n\n"
        f"👤 {user.mention}\n"
        f"🆔 `{user.id}`\n"
        f"💬 {username}\n"
        f"🏷 {chat.title}\n\n"
        f"Choose an action below."
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Accept",
                    callback_data=f"approve|{chat.id}|{user.id}"
                ),
                InlineKeyboardButton(
                    "❌ Decline",
                    callback_data=f"decline|{chat.id}|{user.id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "👤 View Profile",
                    url=f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"
                )
            ]
        ]
    )

    photo = None

    try:
        photos = await client.get_profile_photos(user.id, limit=1)

        if photos.total > 0:
            photo = photos.photos[0][-1].file_id

    except Exception:
        pass

    try:

        if photo:

            await client.send_photo(
                LOG_CHANNEL_ID,
                photo=photo,
                caption=caption,
                reply_markup=buttons,
                parse_mode=ParseMode.MARKDOWN
            )

        else:

            await client.send_message(
                LOG_CHANNEL_ID,
                caption,
                reply_markup=buttons,
                parse_mode=ParseMode.MARKDOWN
            )

    except FloodWait as e:
        await asyncio.sleep(e.value)


# ===============================
# APPROVE / DECLINE HANDLER
# ===============================

@app.on_callback_query(filters.regex("^(approve|decline)\\|"))
async def join_request_buttons(client, callback):

    action, chat_id, user_id = callback.data.split("|")

    chat_id = int(chat_id)
    user_id = int(user_id)

    admin = callback.from_user

    try:

        if action == "approve":

            await client.approve_chat_join_request(chat_id, user_id)

            text = (
                f"🌟 **Request Approved**\n\n"
                f"👤 User: `{user_id}`\n"
                f"✅ Approved By: {admin.mention}\n\n"
                f"User can now join the group."
            )

        else:

            await client.decline_chat_join_request(chat_id, user_id)

            text = (
                f"🚫 **Request Declined**\n\n"
                f"👤 User: `{user_id}`\n"
                f"❌ Declined By: {admin.mention}"
            )

        try:
            await callback.message.delete()
        except:
            pass

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👤 Open Profile",
                        url=f"tg://user?id={user_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Developer",
                        url=DEVELOPER_URL
                    )
                ]
            ]
        )

        await client.send_message(
            LOG_CHANNEL_ID,
            text,
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )

        await callback.answer("Action Completed")

    except FloodWait as e:

        await asyncio.sleep(e.value)

    except Exception:

        await callback.answer("Error occurred", show_alert=True)
