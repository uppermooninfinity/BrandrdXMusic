from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    enable_antiflood,
    disable_antiflood,
    is_antiflood_enabled
)

from collections import defaultdict
import time

flood = defaultdict(list)


# ─────────────────────────────
# PANEL
# ─────────────────────────────

@app.on_message(filters.command("antiflood") & filters.group)
async def antiflood_panel(_, message):

    user = await app.get_chat_member(message.chat.id, message.from_user.id)

    if not user.privileges or not user.privileges.can_delete_messages:
        return

    chat_id = message.chat.id

    if await is_antiflood_enabled(chat_id):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔴 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝖠𝗇𝗍𝗂𝖥𝗅𝗈𝗈𝖽",
                        callback_data=f"antiflood_disable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**🌊 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝗂𝗌 𝖤𝗇𝖺𝖻𝗅𝖾𝖽.**",
            reply_markup=buttons
        )

    else:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 𝖤𝗇𝖺𝖻𝗅𝖾 𝖠𝗇𝗍𝗂𝖥𝗅𝗈𝗈𝖽",
                        callback_data=f"antiflood_enable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**⚠️ 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝗂𝗌 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**",
            reply_markup=buttons
        )


# ─────────────────────────────
# BUTTON
# ─────────────────────────────

@app.on_callback_query(filters.regex("antiflood_"))
async def antiflood_toggle(_, query):

    data = query.data.split(":")
    action = data[0]
    chat_id = int(data[1])

    if action == "antiflood_enable":

        await enable_antiflood(chat_id)

        await query.message.edit_text(
            "**🟢 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝖤𝗇𝖺𝖻𝗅𝖾𝖽.**"
        )

    elif action == "antiflood_disable":

        await disable_antiflood(chat_id)

        await query.message.edit_text(
            "**🔴 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**"
        )


# ─────────────────────────────
# FLOOD PROTECTION
# ─────────────────────────────

@app.on_message(filters.group)
async def antiflood_protection(_, message):

    chat_id = message.chat.id

    if not await is_antiflood_enabled(chat_id):
        return

    user_id = message.from_user.id

    now = time.time()

    flood[user_id].append(now)

    flood[user_id] = [x for x in flood[user_id] if now - x < 5]

    if len(flood[user_id]) > 6:

        try:

            await message.chat.restrict_member(
                user_id,
                permissions=message.chat.permissions
            )

            await message.reply_text(
                f"🚫 {message.from_user.mention} **Muted for Flooding.**"
            )

        except ChatAdminRequired:
            pass


__MODULE__ = "𝖠𝗇𝗍𝗂𝖥𝗅𝗈𝗈𝖽"

__HELP__ = """
**🌊 𝖠𝗇𝗍𝗂-𝖥𝗅𝗈𝗈𝖽**

/antiflood

➤ 𝖯𝗋𝖾𝗏𝖾𝗇𝗍𝗌 𝗌𝗉𝖺𝗆  
➤ 𝖠𝗎𝗍𝗈 𝗆𝗎𝗍𝖾 𝖿𝗅𝗈𝗈𝖽𝖾𝗋𝗌
"""
