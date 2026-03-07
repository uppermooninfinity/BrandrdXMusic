from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from BrandrdXMusic import app


@app.on_callback_query(filters.regex("clone_manager"))
async def clone_manager_callback(client, query):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🤖 ᴄʟᴏɴᴇ ʙᴏᴛ", callback_data="clone_bot")
            ],
            [
                InlineKeyboardButton("📜 sᴇᴇ ᴄʟᴏɴᴇᴅ", callback_data="see_clones")
            ],
            [
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ", callback_data="remove_clone")
            ],
            [
                InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_help")
            ],
        ]
    )

    await query.message.edit_text(
        "⚙️ **ᴄʟᴏɴᴇ ϻᴧηᴧɢєϻєηᴛ**\n\n"
        "Manage your cloned bots easily.\n\n"
        "Choose an option below:",
        reply_markup=buttons
    )
