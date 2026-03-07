from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    enable_antichannel,
    disable_antichannel,
    is_antichannel_enabled
)


# ─────────────────────────────
# PANEL COMMAND
# ─────────────────────────────

@app.on_message(filters.command("antichannel") & filters.group)
async def antichannel_panel(_, message):

    user = await app.get_chat_member(message.chat.id, message.from_user.id)

    if not user.privileges or not user.privileges.can_delete_messages:
        return

    chat_id = message.chat.id

    if await is_antichannel_enabled(chat_id):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔴 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝖠𝗇𝗍𝗂𝗖𝗁𝖺𝗇𝗇𝖾𝗅",
                        callback_data=f"antich_disable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**🛡️ 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝖤𝗇𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖦𝗋𝗈𝗎𝗉.**",
            reply_markup=buttons
        )

    else:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 𝖤𝗇𝖺𝖻𝗅𝖾 𝖠𝗇𝗍𝗂𝗖𝗁𝖺𝗇𝗇𝖾𝗅",
                        callback_data=f"antich_enable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**⚠️ 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖦𝗋𝗈𝗎𝗉.**",
            reply_markup=buttons
        )


# ─────────────────────────────
# BUTTON HANDLER
# ─────────────────────────────

@app.on_callback_query(filters.regex("antich_"))
async def antichannel_toggle(_, query):

    data = query.data.split(":")
    action = data[0]
    chat_id = int(data[1])

    if action == "antich_enable":

        await enable_antichannel(chat_id)

        await query.message.edit_text(
            "**🟢 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗁𝖺𝗌 𝖡𝖾𝖾𝗇 𝖤𝗇𝖺𝖻𝗅𝖾𝖽.**"
        )

    elif action == "antich_disable":

        await disable_antichannel(chat_id)

        await query.message.edit_text(
            "**🔴 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗁𝖺𝗌 𝖡𝖾𝖾𝗇 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**"
        )


# ─────────────────────────────
# MAIN PROTECTION
# ─────────────────────────────

@app.on_message(filters.group)
async def antichannel_protection(_, message):

    chat_id = message.chat.id

    if not await is_antichannel_enabled(chat_id):
        return

    if not message.sender_chat:
        return

    # ignore linked discussion channel
    chat = await app.get_chat(chat_id)

    if chat.linked_chat and message.sender_chat.id == chat.linked_chat.id:
        return

    try:

        await app.ban_chat_member(chat_id, message.sender_chat.id)

        await message.reply_text(
            "**🚫 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖯𝗋𝗈𝖿𝗂𝗅𝖾 𝖨𝗌 𝖭𝗈𝗍 𝖠𝗅𝗅𝗈𝗐𝖾𝖽.**\n"
            "> 𝖠𝗎𝗍𝗈 𝖲𝖾𝖼𝗎𝗋𝗂𝗍𝗒 𝖲𝗒𝗌𝗍𝖾𝗆 𝖠𝖼𝗍𝗂𝗏𝖾."
        )

    except ChatAdminRequired:

        await message.reply_text(
            "**⚠️ 𝖨 𝖭𝖾𝖾𝖽 𝖡𝖺𝗇 𝖴𝗌𝖾𝗋𝗌 𝖯𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇.**"
        )


# ─────────────────────────────

__MODULE__ = "𝖠𝗇𝗍𝗂𝖢𝗁𝖺𝗇𝗇𝖾𝗅"

__HELP__ = """
**🛡️ 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅**

✧ /antichannel

𝖤𝗇𝖺𝖻𝗅𝖾𝗌 𝗈𝗋 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝗌 𝖠𝗇𝗍𝗂-𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇.

➤ 𝖡𝗅𝗈𝖼𝗄𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖯𝗋𝗈𝖿𝗂𝗅𝖾𝗌
➤ 𝖠𝗎𝗍𝗈 𝖡𝖺𝗇𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌
➤ 𝖲𝖾𝖼𝗎𝗋𝗂𝗍𝗒 𝖥𝗈𝗋 𝖦𝗋𝗈𝗎𝗉𝗌
"""
