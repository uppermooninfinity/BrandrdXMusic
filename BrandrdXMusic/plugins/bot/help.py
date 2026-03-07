import config
from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS, SUPPORT_CHAT
from BrandrdXMusic import app
from BrandrdXMusic.utils import help_pannel
from BrandrdXMusic.utils.database import get_lang
from BrandrdXMusic.utils.decorators.language import LanguageStart, languageCB
from BrandrdXMusic.utils.inline.help import help_back_markup, private_help_panel
from BrandrdXMusic.utils.stuffs.buttons import BUTTONS
from BrandrdXMusic.utils.stuffs.helper import Helper
from strings import get_string, helpers
from pyrogram.types import CallbackQuery

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)

        await update.reply_video(
            video="https://files.catbox.moe/ix1sik.mp4",
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_photo(
    photo=config.HELP_IMG_URL,
    caption=(
        "❖ ʜᴇʟᴘ ᴍᴀɪɴ ᴍᴇɴᴜ ❖\n\n"
        "✦ ᴄʜσσsє ᴛʜє ᴄᴧᴛєɢσʀʏ ꜰσʀ ᴡʜɪᴄʜ ʏσᴜ ᴡᴧηηᴧ ɢєᴛ ʜєʟᴘ 🎀✨"
    ),
    reply_markup=help_pannel(_)
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
    elif cb == "hb16":
        await CallbackQuery.edit_message_text(helpers.HELP_16, reply_markup=keyboard)
    elif cb == "hb17":
        await CallbackQuery.edit_message_text(helpers.HELP_17, reply_markup=keyboard)
    elif cb == "hb18":
        await CallbackQuery.edit_message_text(helpers.HELP_18, reply_markup=keyboard)
    elif cb == "hb19":
        await CallbackQuery.edit_message_text(helpers.HELP_19, reply_markup=keyboard)
    elif cb == "hb20":
        await CallbackQuery.edit_message_text(helpers.HELP_20, reply_markup=keyboard)
    elif cb == "hb21":
        await CallbackQuery.edit_message_text(helpers.HELP_21, reply_markup=keyboard)


@app.on_callback_query(filters.regex("mbot_cb") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_M, reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON)
    )


@app.on_callback_query(filters.regex("managebot123"))
async def on_back_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_pannel(_, True)
    if cb == "settings_back_helper":
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )

# ==============================
# MAIN HELP CATEGORY HANDLERS
# ==============================

@app.on_callback_query(filters.regex("^HELP_MANAGEMENT$") & ~BANNED_USERS)
async def help_management(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(
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
    
    await query.message.edit_text(
        "• ϻᴧηᴧɢєϻєηᴛ •\n\n"
        "✦ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs\n"
        "✦ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n"
        "✦ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ sʏsᴛᴇᴍ\n\n"
        "Manage your groups easily with these commands.",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^HELP_VIDEOCHAT$") & ~BANNED_USERS)
async def help_videochat(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(
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
    
    await query.message.edit_text(
        "• ᴠɪᴅєσᴄʜᴧᴛ •\n\n"
        "✦ ᴘʟᴀʏ ᴍᴜsɪᴄ\n"
        "✦ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ\n"
        "✦ ᴠᴄ ᴄᴏɴᴛʀᴏʟ\n\n"
        "Stream music & video inside voice chats.",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^HELP_FUN$") & ~BANNED_USERS)
async def help_fun(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(
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
    
    await query.message.edit_text(
        "• ꜰᴜη •\n\n"
        "✦ ᴇɴᴛᴇʀᴛᴀɪɴᴍᴇɴᴛ ᴄᴏᴍᴍᴀɴᴅs\n"
        "✦ ɢʀᴏᴜᴘ ғᴜη\n"
        "✦ ʀᴀɴᴅᴏᴍ ғᴜη ᴛᴏᴏʟs\n\n"
        "Enjoy fun commands with your friends.",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^HELP_SUDOERS$") & ~BANNED_USERS)
async def help_sudoers(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(
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
    await query.message.edit_text(
        "• ꜱᴜᴅσєʀꜱ •\n\n"
        "✦ ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅs\n"
        "✦ ʙᴏᴛ ᴄᴏɴᴛʀᴏʟ\n"
        "✦ sʏsᴛᴇᴍ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n\n"
        "These commands are restricted to bot sudo users.",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^clone_manager$") & ~BANNED_USERS)
async def help_clone(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🤖 ᴄʟᴏɴᴇ ʙᴏᴛ", callback_data="clone_bot")
            ],
            [
                InlineKeyboardButton("📜 sᴇᴇ ᴄʟᴏɴᴇᴅ", callback_data="see_clones")
            ],
            [
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ", callback_data="remove_clone")
            ],
            [
                InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_help")
            ],
        ]
    )
    await query.message.edit_text(
        "• ᴄʟᴏɴᴇ ϻᴧηᴧɢєϻєηᴛ •\n\n"
        "✦ ᴄʀᴇᴀᴛᴇ ʙᴏᴛ ᴄʟᴏɴᴇ\n"
        "✦ sᴇᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛs\n"
        "✦ ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ\n\n"
        "Commands:\n"
        "`/clone BOT_TOKEN`\n"
        "`/mybots`\n"
        "`/rmclone BOT_ID`",
        reply_markup=keyboard
    )



@app.on_callback_query(filters.regex("^back_to_main$") & ~BANNED_USERS)
async def back_to_main_handler(client, query: CallbackQuery):

    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    keyboard = help_back_markup(_)

    await query.message.edit_text(
        "Choose the category for which you wanna get help",
        reply_markup=help_pannel(_),
    )
    
@app.on_callback_query(filters.regex("mplus"))
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"mbot_cb")]]
    )
    if cb == "Okieeeeee":
        await CallbackQuery.edit_message_text(
            f"`something errors`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN,
        )
    else:
        await CallbackQuery.edit_message_text(
            getattr(Helper, cb), reply_markup=keyboard
        )
