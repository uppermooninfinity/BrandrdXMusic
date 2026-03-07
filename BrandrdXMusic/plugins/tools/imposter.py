from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    save_or_check_user,
    is_imposter_enabled,
    enable_imposter,
    disable_imposter
)


# ─────────────────────────────
# PANEL COMMAND
# ─────────────────────────────

@app.on_message(filters.command("imposter") & filters.group)
async def imposter_panel(_, message):

    user = await app.get_chat_member(message.chat.id, message.from_user.id)

    if not user.privileges or not user.privileges.can_delete_messages:
        return

    chat_id = message.chat.id

    if await is_imposter_enabled(chat_id):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔴 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋",
                        callback_data=f"imposter_disable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**🕵️ 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇 𝗂𝗌 𝖤𝗇𝖺𝖻𝗅𝖾𝖽.**",
            reply_markup=buttons
        )

    else:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 𝖤𝗇𝖺𝖻𝗅𝖾 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋",
                        callback_data=f"imposter_enable:{chat_id}"
                    )
                ]
            ]
        )

        await message.reply_text(
            "**⚠️ 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇 𝗂𝗌 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**",
            reply_markup=buttons
        )


# ─────────────────────────────
# BUTTON HANDLER
# ─────────────────────────────

@app.on_callback_query(filters.regex("imposter_"))
async def imposter_toggle(_, query):

    data = query.data.split(":")
    action = data[0]
    chat_id = int(data[1])

    if action == "imposter_enable":

        chat = await app.get_chat(chat_id)

        await enable_imposter(chat_id, chat.title, chat.username)

        await query.message.edit_text(
            "**🟢 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇 𝖤𝗇𝖺𝖻𝗅𝖾𝖽.**"
        )

    elif action == "imposter_disable":

        await disable_imposter(chat_id)

        await query.message.edit_text(
            "**🔴 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽.**"
        )


# ─────────────────────────────
# PROFILE CHANGE DETECTION
# ─────────────────────────────

@app.on_message(filters.group)
async def imposter_detection(_, message):

    chat_id = message.chat.id

    if not await is_imposter_enabled(chat_id):
        return

    user = message.from_user
    if not user:
        return

    changes = await save_or_check_user(user)

    if changes:

        text = ""

        for field, old, new in changes:

            text += (
                f"• **{field.capitalize()} Updated**\n"
                f"  ├ 𝖯𝗋𝖾𝗏𝗂𝗈𝗎𝗌 : `{old}`\n"
                f"  └ 𝖭𝖾𝗐 : `{new}`\n\n"
            )

        alert = (
            f"🚨 **𝖴𝗌𝖾𝗋 𝖯𝗋𝗈𝖿𝗂𝗅𝖾 𝖢𝗁𝖺𝗇𝗀𝖾 𝖣𝖾𝗍𝖾𝖼𝗍𝖾𝖽**\n\n"
            f"👤 {user.mention}\n"
            f"🆔 `{user.id}`\n\n"
            f"{text}"
        )

        await message.reply_text(alert)


__MODULE__ = "𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋"

__HELP__ = """
**🕵️ 𝖨𝗆𝗉𝗈𝗌𝗍𝖾𝗋 𝖯𝗋𝗈𝗍𝖾𝖼𝗍𝗂𝗈𝗇**

/imposter

➤ 𝖳𝗋𝖺𝖼𝗄𝗌 𝗎𝗌𝖾𝗋 𝗉𝗋𝗈𝖿𝗂𝗅𝖾 𝖼𝗁𝖺𝗇𝗀𝖾𝗌  
➤ 𝖣𝖾𝗍𝖾𝖼𝗍𝗌 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾 / 𝗇𝖺𝗆𝖾 𝗎𝗉𝖽𝖺𝗍𝖾𝗌  
➤ 𝖠𝗅𝖾𝗋𝗍𝗌 𝗀𝗋𝗈𝗎𝗉
"""
