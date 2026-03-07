from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app


# =========================
# MAIN HELP PANEL (4 MAIN BUTTONS)
# =========================

def help_pannel(_, START: Union[bool, int] = None):
    first = [
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    ]

    second = [
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper"),
        ]
    ]

    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• ᴠɪᴅєσᴄʜᴧᴛ •", callback_data="HELP_VIDEOCHAT"),
                InlineKeyboardButton(" • ꜰᴜη •", callback_data="HELP_FUN"),
            ],
            [
                InlineKeyboardButton("• ϻᴧηᴧɢєϻєηᴛ •", callback_data="HELP_MANAGEMENT"),
                InlineKeyboardButton("• ꜱᴜᴅσєʀꜱ σηʟʏ •", callback_data="HELP_SUDOERS"),
            ],
            [
                InlineKeyboardButton("• ϻᴧηᴧɢєϻєηᴛ ᴄʟᴏηє •", callback_data="clone_manager")
            ]
            *mark,
        ]
    )
    return upl

def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="back_to_main",
                ),
            ]
        ]
    )


# =========================
# PRIVATE HELP PANEL
# =========================

def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
