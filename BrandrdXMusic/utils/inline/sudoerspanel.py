from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

def sudoers_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
            ],
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )
