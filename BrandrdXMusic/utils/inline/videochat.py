from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

def videochat_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15"),
            ],
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )
