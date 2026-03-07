from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from BrandrdXMusic import app


# =========================
# CLONE MANAGER PANEL
# =========================

def clone_manager_panel():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🤖 ᴄʟᴏɴᴇ ʙᴏᴛ",
                    callback_data="clone_create"
                )
            ],
            [
                InlineKeyboardButton(
                    "📜 sᴇᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛs",
                    callback_data="clone_list"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ",
                    callback_data="clone_delete"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 ʙᴀᴄᴋ",
                    callback_data="back_to_main"
                )
            ],
        ]
    )


# =========================
# OPEN CLONE PANEL
# =========================

@app.on_callback_query(filters.regex("^clone_manager$"))
async def clone_manager_handler(client, callback_query):

    text = (
        "🤖 **ᴄʟᴏɴᴇ ϻᴧηᴧɢєϻєηᴛ**\n\n"
        "Manage your cloned bots easily.\n\n"
        "• Create new clone\n"
        "• View cloned bots\n"
        "• Remove clone bot"
    )

    await callback_query.message.edit_text(
        text,
        reply_markup=clone_manager_panel()
    )

    await callback_query.answer()


# =========================
# BUTTON RESPONSES
# =========================

@app.on_callback_query(filters.regex("^clone_create$"))
async def clone_create_handler(client, callback_query):

    await callback_query.answer()

    await callback_query.message.edit_text(
        "🤖 **Clone Bot**\n\n"
        "Use this command to create a clone:\n\n"
        "`/clone BOT_TOKEN`",
        reply_markup=clone_manager_panel()
    )


@app.on_callback_query(filters.regex("^clone_list$"))
async def clone_list_handler(client, callback_query):

    await callback_query.answer()

    await callback_query.message.edit_text(
        "📜 **Your Cloned Bots**\n\n"
        "Use this command:\n\n"
        "`/mybots`",
        reply_markup=clone_manager_panel()
    )


@app.on_callback_query(filters.regex("^clone_delete$"))
async def clone_delete_handler(client, callback_query):

    await callback_query.answer()

    await callback_query.message.edit_text(
        "❌ **Remove Clone Bot**\n\n"
        "Use this command:\n\n"
        "`/delclone @botusername`",
        reply_markup=clone_manager_panel()
    )
