from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.decorator.chatadmin import chatadmin
from BrandrdXMusic.decorator.errors import error

# Hardcoded prefixes: / ! .
PREFIXES = ["/", "!", "."]

@app.on_message(filters.command("link", prefixes=PREFIXES) & filters.group)
@chatadmin
@error
async def chat_link_handler(client, message: Message):
    """
    /link <chat_id> - Get invite link for a chat.
    Only admins can use this command.
    """

    # Extract chat_id from message
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Please provide a chat ID. Example:\n`/link -1001234567890`"
        )
        return

    chat_id = message.command[1]

    try:
        chat = await client.get_chat(chat_id)
        
        # Only supergroups or channels
        if chat.type in ["supergroup", "channel"]:
            try:
                invite_link = await client.export_chat_invite_link(chat_id)
                await message.reply_text(
                    f"🔗 **Invite Link for {chat.title}:**\n{invite_link}"
                )
            except Exception as e:
                await message.reply_text(f"❌ Failed to get link. Error:\n`{e}`")
        else:
            await message.reply_text("❌ This command only works for supergroups or channels.")
    except Exception as e:
        await message.reply_text(f"❌ Invalid chat ID or bot is not in that chat.\n`{e}`")
