import asyncio

from BrandrdXMusic import app
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import MUSIC_BOT_NAME

@app.on_message(filters.command(["alive"]))
async def start(client: Client, message: Message):
    await message.reply_video(
        video=f"https://files.catbox.moe/xv6obl.mp4",
        caption=f"<blockquote>🪷 ʜᴇʏ {message.from_user.mention}</blockquote>\n\n<blockquote expandable>🌷 ɪ ᴀᴍ {MUSIC_BOT_NAME}\n\n✨ ɪ ᴀᴍ ғᴀsᴛ ᴀɴᴅ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.\n\n💫 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ ᴊᴏɪɴ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ🤍...\n\n━━━━━━━━━━━━━━━━━━❄</blockquote expandable>",
        reply_markup=InlineKeyboardMarkup(
            [
               [
            InlineKeyboardButton(
                text="˹ ɪɴꜰɪɴɪᴛʏ ɴᴇᴛᴡᴏʀᴋ˼  ", url=f"https://t.me/dark_musictm"
            ),
            InlineKeyboardButton(
                text="˹ | • ɪɴғɪɴɪᴛʏ • | ˼", url=f"https://t.me/cyber_github"
            ),
        ],
                [
            InlineKeyboardButton(
                text="ʏᴜᴋɪᴇᴇ's ʜᴏᴍᴇᴛᴏᴡɴ 🌷", url=f"https://t.me/yukieee_03"
            ),
                ],
                [
                    InlineKeyboardButton(
                        "✯ᴄʟᴏsᴇ✯", callback_data="close"
                    )
                ],
            ]
        )
    )
