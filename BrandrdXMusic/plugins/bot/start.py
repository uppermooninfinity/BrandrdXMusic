import time
import asyncio
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string
from BrandrdXMusic.misc import SUDOERS

NEXI_VID = [
"https://files.catbox.moe/ylwfbj.mp4",
"https://files.catbox.moe/k8lr4l.mp4",
"https://files.catbox.moe/pbrp19.mp4",
"https://files.catbox.moe/yvhhae.mp4",
"https://files.catbox.moe/y25m1l.mp4",
"https://files.catbox.moe/mbqcej.mp4",

]

STICKER = [
    "CAACAgUAAxkBAAEQqkpppuCcBlyBAAGAJ706ZK6zkQnpL88AAi0aAAIyYClUfH4DPEThazk6BA",
    "CAACAgUAAxkBAAEQEGVpSR-TuCKHP8D69SvDAAH2Gn7QjXEAAtIEAAKP9uhXzLPwoqMKxuQ2BA",
    "CAACAgUAAxkBAAEQEGVpSR-TuCKHP8D69SvDAAH2Gn7QjXEAAtIEAAKP9uhXzLPwoqMKxuQ2BA",
]

EMOJIOS = ["🚩", "🥀", "🪄", "🩷", "⚡", "❤️‍🩹", "🩶", "🩵", "💜", "🕊"]


# 
# ==============================
# PRIVATE START
# ==============================

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(message.from_user.id)
    await message.react("❤")
     
    accha = await message.reply_text(text=random.choice(EMOJIOS))
    await asyncio.sleep(1.3)
    await accha.edit("🔊 ᴘʟєᴧꜱє ᴡᴧɪᴛ... ʟєᴛ ᴛʜє ᴠɪʙєꜱ ʙєɢɪη 💫")
    await asyncio.sleep(0.2)
    await accha.edit(" ˹ ᴏɴᴇ ғᴏʀ ᴀʟʟ ꜱᴛᴧʀᴛɪηɢ ✨🎶˼")
    await asyncio.sleep(0.2)
    await accha.edit("__.ʜєʟʟσ ʜσω ᴧʀє ʏσᴜ 🩷 .__")
    await asyncio.sleep(0.2)
    await accha.delete()

    umm = await message.reply_sticker(sticker=random.choice(STICKER))
    await asyncio.sleep(2)
    await umm.delete()

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_video(
                random.choice(NEXI_VID),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="˹ ɪɴꜰɪɴɪᴛʏ ✘ ɴᴇᴛᴡᴏʀᴋ˼ 🎧", url="https://t.me/dark_musictm"),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=config.YOUTUBE_IMG_URL,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await message.reply_video(
            random.choice(NEXI_VID),
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


# ====


# ==============================
# GROUP START (UNCHANGED)
# ==============================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(NEXI_VID),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)
