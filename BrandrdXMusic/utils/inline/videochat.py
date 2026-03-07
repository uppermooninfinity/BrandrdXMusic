from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from BrandrdXMusic import app


# =========================
# VIDEOCHAT PANEL
# =========================

def videochat_panel(_):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_["H_B_6"], callback_data="help_callback hb6"),
                InlineKeyboardButton(_["H_B_11"], callback_data="help_callback hb11"),
                InlineKeyboardButton(_["H_B_12"], callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(_["H_B_13"], callback_data="help_callback hb13"),
                InlineKeyboardButton(_["H_B_14"], callback_data="help_callback hb14"),
                InlineKeyboardButton(_["H_B_15"], callback_data="help_callback hb15"),
            ],
            [
                InlineKeyboardButton(_["BACK_BUTTON"], callback_data="back_to_main")
            ]
        ]
    )


# =========================
# CALLBACK HANDLER
# =========================

@app.on_callback_query(filters.regex("videochat"))
async def videochat_callback(client, callback_query):

    _ = callback_query._  # language dict if you are using language system

    await callback_query.message.edit_text(
        _["HELP_VIDEOCHAT"],
        reply_markup=videochat_panel(_)
    )

    await callback_query.answer()
