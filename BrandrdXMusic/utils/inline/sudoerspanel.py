from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from BrandrdXMusic import app


# =========================
# SUDOERS PANEL
# =========================

def sudoers_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_["H_B_7"], callback_data="help_callback hb7"),
                InlineKeyboardButton(_["H_B_4"], callback_data="help_callback hb4"),
            ],
            [
                InlineKeyboardButton(_["H_B_3"], callback_data="help_callback hb3"),
                InlineKeyboardButton(_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(_["H_B_5"], callback_data="help_callback hb5"),
            ],
            [
                InlineKeyboardButton(_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )


# =========================
# CALLBACK HANDLER
# =========================

@app.on_callback_query(filters.regex("sudoers"))
async def sudoers_callback(client, callback_query):

    _ = callback_query._

    await callback_query.message.edit_text(
        _["HELP_SUDOERS"],
        reply_markup=sudoers_panel(_)
    )

    await callback_query.answer()
