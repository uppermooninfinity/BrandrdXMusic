from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from BrandrdXMusic import app


# =========================
# MODERATION PANEL
# =========================

def moderation_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(_["H_B_9"], callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(_["H_B_18"], callback_data="help_callback hb18"),
                InlineKeyboardButton(_["H_B_20"], callback_data="help_callback hb20"),
                InlineKeyboardButton(_["H_B_24"], callback_data="help_callback hb24"),
            ],
            [
                InlineKeyboardButton(_["H_B_28"], callback_data="help_callback hb28"),
            ],
            [
                InlineKeyboardButton(_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )


# =========================
# CALLBACK HANDLER
# =========================

@app.on_callback_query(filters.regex("management"))
async def moderation_callback(client, callback_query):

    _ = callback_query._

    await callback_query.message.edit_text(
        _["HELP_MODERATION"],
        reply_markup=moderation_panel(_)
    )

    await callback_query.answer()
