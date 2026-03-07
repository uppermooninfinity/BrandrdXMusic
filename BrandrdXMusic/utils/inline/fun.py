from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from BrandrdXMusic import app


# =========================
# FUN PANEL
# =========================

def fun_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_["H_B_16"], callback_data="help_callback hb16"),
                InlineKeyboardButton(_["H_B_17"], callback_data="help_callback hb17"),
                InlineKeyboardButton(_["H_B_22"], callback_data="help_callback hb22"),
            ],
            [
                InlineKeyboardButton(_["H_B_25"], callback_data="help_callback hb25"),
                InlineKeyboardButton(_["H_B_27"], callback_data="help_callback hb27"),
                InlineKeyboardButton("✨ ғsᴜʙ", callback_data="help_callback hb20"),
                InlineKeyboardButton("🎮 ғᴜɴ ɢᴀᴍᴇ", callback_data="help_callback hb26"),
            ],
            [
                InlineKeyboardButton(_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )


# =========================
# CALLBACK HANDLER
# =========================

@app.on_callback_query(filters.regex("fun"))
async def fun_callback(client, callback_query):

    _ = callback_query._

    await callback_query.message.edit_text(
        _["HELP_FUN"],
        reply_markup=fun_panel(_)
    )

    await callback_query.answer()
