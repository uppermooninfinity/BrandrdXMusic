from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def fun_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16"),
                InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17"),
                InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25"),
                InlineKeyboardButton(text=_["H_B_27"], callback_data="help_callback hb27"),
                InlineKeyboardButton(text="✨ ғsᴜʙ",callback_data="help_callback hb20"),
                InlineKeyboardButton(text="🎮 ғᴜɴ ɢᴀᴍᴇ",callback_data="help_callback hb26"),
            ],
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )
