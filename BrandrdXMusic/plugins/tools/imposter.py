from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    save_or_check_user,
    is_imposter_enabled,
    enable_imposter,
    disable_imposter,
)

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import config
from BrandrdXMusic.decorator.chatadmin import chatadmin
from BrandrdXMusic.decorator.save import save
from BrandrdXMusic.decorator.errors import error


# Command to toggle imposter status
@app.on_message(filters.command("imposter", prefixes=config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def imposter_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if await is_imposter_enabled(chat_id):
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔴 Disable 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋",
                        callback_data=f"disable_imposter:{chat_id}",
                    )
                ],
                [InlineKeyboardButton("🗑️", callback_data="delete")],
            ]
        )
        await message.reply_text(
            "**📢 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 is enabled in this chat.**",
            reply_markup=button,
        )
    else:
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 Enable 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋",
                        callback_data=f"enable_imposter:{chat_id}",
                    )
                ],
                [InlineKeyboardButton("🗑️", callback_data="delete")],
            ]
        )
        await message.reply_text(
            "**📢 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 is disabled in this chat.**",
            reply_markup=button,
        )


# Callback query handler
@app.on_callback_query(filters.regex("^(enable_imposter|disable_imposter):"))
@chatadmin
@error
async def toggle_imposters(client: Client, callback_query: CallbackQuery):
    action, chat_id = callback_query.data.split(":")
    chat_id = int(chat_id)

    chat = await client.get_chat(chat_id)

    if action == "enable_imposter":
        await enable_imposter(chat_id, chat.title, chat.username)
        await callback_query.message.edit_text(
            "**🟢 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 has been enabled for this chat.**"
        )

    elif action == "disable_imposter":
        await disable_imposter(chat_id)
        await callback_query.message.edit_text(
            "**🔴 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 has been disabled for this chat.**"
        )


# Detect profile changes
@app.on_message(filters.group, group=IMPOSTER_GROUP)
@error
@save
async def imposter_text_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if not await is_imposter_enabled(chat_id):
        return

    user = message.from_user
    if not user:
        return

    changes = await save_or_check_user(user)

    if changes:
        change_details = "\n".join(
            f"• **{field.capitalize()}:**\n"
            f"   - **Previous:** {old if old else 'None'}\n"
            f"   - **Updated:** {new if new else 'None'}"
            for field, old, new in changes
        )

        announcement = (
            f"🔔 **User Profile Update Detected**\n\n"
            f"👤 **User:** {user.mention()} ({user.id})\n\n"
            f"{change_details}"
        )

        await message.reply_text(
            announcement,
            disable_web_page_preview=True,
        )


__module__ = "Imposter"


__help__ = """
**Purpose:**
This module monitors changes in user profile information in group chats.

**Features:**
✧ Tracks changes in:
  - Username
  - First Name
  - Last Name

✧ Sends notification in group when a user updates profile details.

**Command:**
/imposter - Enable or disable imposter detection
"""
