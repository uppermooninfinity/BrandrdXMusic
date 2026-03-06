import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from collections import defaultdict
from time import time

from BrandrdXMusic import app

# Anti Spam Config
SPAM_LIMIT = 5
SPAM_TIME = 8
WARN_LIMIT = 3
AUTO_DELETE_TIME = 15

# Memory storage
user_msgs = defaultdict(list)
user_warns = defaultdict(int)


def smallcaps(text: str):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    table = str.maketrans(normal, small)
    return text.translate(table)


QUOTE1 = smallcaps("spam destroys conversations")
QUOTE2 = smallcaps("respect the chat, respect the vibe")
QUOTE3 = smallcaps("good music deserves good behaviour")


def warn_text(user, warns):
    return f"""
⚠️ <b>{smallcaps("warning issued")}</b>

<blockquote>{QUOTE1}</blockquote>
<blockquote>{QUOTE2}</blockquote>
<blockquote>{QUOTE3}</blockquote>

━━━━━━━━━━━━━━━━━━
<b>{smallcaps("user")}:</b> {user}
<b>{smallcaps("warns")}:</b> {warns}/{WARN_LIMIT}
━━━━━━━━━━━━━━━━━━

<i>{smallcaps("please avoid spamming messages")}</i>
"""


@app.on_message(filters.group & ~filters.bot)
async def antispam_handler(_, message: Message):

    user_id = message.from_user.id
    now = time()

    user_msgs[user_id] = [
        msg_time for msg_time in user_msgs[user_id]
        if now - msg_time < SPAM_TIME
    ]

    user_msgs[user_id].append(now)

    if len(user_msgs[user_id]) > SPAM_LIMIT:

        user_warns[user_id] += 1
        warns = user_warns[user_id]

        text = warn_text(message.from_user.mention, warns)

        warn_msg = await message.reply_text(
            text,
            parse_mode=ParseMode.HTML
        )

        await asyncio.sleep(AUTO_DELETE_TIME)
        await warn_msg.delete()

        user_msgs[user_id] = []

        if warns >= WARN_LIMIT:
            try:
                await message.chat.ban_member(user_id)

                ban_text = f"""
🚫 <b>{smallcaps("user banned for spam")}</b>

<blockquote>{QUOTE1}</blockquote>

<b>{smallcaps("user")}:</b> {message.from_user.mention}
"""

                ban_msg = await message.reply_text(
                    ban_text,
                    parse_mode=ParseMode.HTML
                )

                await asyncio.sleep(AUTO_DELETE_TIME)
                await ban_msg.delete()

            except Exception:
                pass
