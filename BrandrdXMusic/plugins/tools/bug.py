from pyrogram import filters
from pyrogram.enums import ParseMode
from BrandrdXMusic import app

BUG_LOG_CHANNEL = -1003700186680 # put your log channel id


@app.on_message(filters.command("bug") & filters.reply)
async def bug_report(_, message):

    user = message.from_user
    replied = message.reply_to_message

    content = replied.text or replied.caption or "No text content"

    media = (
        "Yes"
        if replied.photo
        or replied.video
        or replied.document
        or replied.animation
        or replied.audio
        else "No"
    )

    username = f"@{user.username}" if user.username else user.mention

    bug_text = f"""
**🐞 𝖡𝗎𝗀 𝖱𝖾𝗉𝗈𝗋𝗍 𝖱𝖾𝖼𝖾𝗂𝗏𝖾𝖽**

**👤 𝖴𝗌𝖾𝗋 :** {username}  
**🆔 𝖨𝖣 :** `{user.id}`

**💬 𝖢𝗁𝖺𝗍 :** {message.chat.title}  
**📎 𝖬𝖾𝖽𝗂𝖺 :** {media}

**📝 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 :**
{content}

**🔗 𝖫𝗂𝗇𝗄 :**
{replied.link}
"""

    await app.send_message(
        BUG_LOG_CHANNEL,
        bug_text,
        parse_mode=ParseMode.MARKDOWN
    )

    await message.reply_text(
        "**✅ 𝖡𝗎𝗀 𝖱𝖾𝗉𝗈𝗋𝗍 𝖲𝖾𝗇𝗍 𝖳𝗈 𝖣𝖾𝗏𝗌.**\n"
        "> 𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝗁𝖾𝗅𝗉𝗂𝗇𝗀 𝗂𝗆𝗉𝗋𝗈𝗏𝖾 𝗍𝗁𝖾 𝖻𝗈𝗍."
    )


@app.on_message(filters.command("bug") & ~filters.reply)
async def bug_usage(_, message):

    await message.reply_text(
        "**⚠️ 𝖴𝗌𝖺𝗀𝖾 :**\n"
        "> 𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗍𝗁 `/bug` 𝗍𝗈 𝗋𝖾𝗉𝗈𝗋𝗍 𝗂𝗍."
    )


__MODULE__ = "𝖡𝗎𝗀"

__HELP__ = """
**🐞 𝖡𝗎𝗀 𝖱𝖾𝗉𝗈𝗋𝗍**

/bug (reply)

→ 𝖱𝖾𝗉𝗈𝗋𝗍 𝖺 𝖻𝗎𝗀 𝗍𝗈 𝗍𝗁𝖾 𝖽𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋𝗌.
"""
