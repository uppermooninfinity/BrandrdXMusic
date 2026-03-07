from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    save_or_check_user,
    is_imposter_enabled,
    enable_imposter,
    disable_imposter,
)

from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import config 

# Enable / Disable imposter command
@app.on_message(filters.command("imposter", prefixes=config.COMMAND_PREFIXES) & filters.group)
async def imposter_handler(_, message: Message):

    # Check admin
    member = await message.chat.get_member(message.from_user.id)
    if not member.privileges:
        return await message.reply_text("❌ **Only admins can use this command.**")

    chat_id = message.chat.id

    if await is_imposter_enabled(chat_id):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔴 Disable Imposter",
                        callback_data=f"disable_imposter:{chat_id}",
                    )
                ]
            ]
        )

        await message.reply_text(
            "**📢 Imposter detection is currently ENABLED in this chat.**",
            reply_markup=keyboard,
        )

    else:

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 Enable Imposter",
                        callback_data=f"enable_imposter:{chat_id}",
                    )
                ]
            ]
        )

        await message.reply_text(
            "**📢 Imposter detection is currently DISABLED in this chat.**",
            reply_markup=keyboard,
        )


# Button handler
@app.on_callback_query(filters.regex("^(enable_imposter|disable_imposter):"))
async def toggle_imposter(_, query: CallbackQuery):

    action, chat_id = query.data.split(":")
    chat_id = int(chat_id)

    member = await query.message.chat.get_member(query.from_user.id)

    if not member.privileges:
        return await query.answer("Only admins can use this.", show_alert=True)

    chat = await app.get_chat(chat_id)

    if action == "enable_imposter":

        await enable_imposter(chat_id, chat.title, chat.username)

        await query.message.edit_text(
            "**🟢 Imposter detection has been ENABLED for this chat.**"
        )

    elif action == "disable_imposter":

        await disable_imposter(chat_id)

        await query.message.edit_text(
            "**🔴 Imposter detection has been DISABLED for this chat.**"
        )


# Detect profile changes
@app.on_message(filters.group)
async def detect_imposter(_, message: Message):

    chat_id = message.chat.id

    if not await is_imposter_enabled(chat_id):
        return

    user = message.from_user
    if not user:
        return

    changes = await save_or_check_user(user)

    if changes:

        change_text = ""

        for field, old, new in changes:
            change_text += (
                f"• **{field.capitalize()} Changed**\n"
                f"  ├ Old : `{old}`\n"
                f"  └ New : `{new}`\n\n"
            )

        alert = (
            f"⚠️ **User Profile Updated**\n\n"
            f"👤 User : {user.mention}\n"
            f"🆔 ID : `{user.id}`\n\n"
            f"{change_text}"
        )

        await message.reply_text(alert)


__MODULE__ = "Imposter"

__HELP__ = """
**Imposter Detection**

Detects when users change their profile.

**Tracks**
• Username
• First Name
• Last Name

**Command**
/imposter - Enable or disable imposter detection
"""
