from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_buttons():
  return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• ᴠɪᴅєσᴄʜᴧᴛ •", callback_data="help_category videochat"),
                InlineKeyboardButton(" • ꜰᴜη •", callback_data="help_category fun"),
            ],
            [
                InlineKeyboardButton("• ϻᴧηᴧɢєϻєηᴛ •", callback_data="help_category moderation"),
                InlineKeyboardButton("• ꜱᴜᴅσєʀꜱ σηʟʏ •", callback_data="help_category sudoers"),
            ],
