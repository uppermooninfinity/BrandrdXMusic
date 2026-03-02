def moderation_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18"),
                InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20"),
                InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_28"], callback_data="help_callback hb28"),
            ],
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="back_to_main"),
            ],
        ]
    )
  
