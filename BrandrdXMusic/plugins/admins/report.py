# plugins/admin/report.py

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

from BrandrdXMusic import app  # change this
from BrandrdXMusic.mongo.report_db import get_settings


def build_report_text(user, chat_title, reported_text, mention_text):
    return (
        f"🚨 **New Report Received**\n\n"
        f"👤 Reporter: {user.mention}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"💬 Group: {chat_title}\n\n"
        f"📩 Reported Content:\n"
        f"{reported_text}\n\n"
        f"{mention_text}"
    )


async def get_admin_mentions(client, chat_id, settings):
    mention_text = ""

    try:
        admins = []
        founder = None

        async for member in client.get_chat_members(chat_id, filter="administrators"):

            if member.user.is_bot:
                continue

            if member.status == ChatMemberStatus.OWNER:
                founder = member.user.mention

            else:
                admins.append(member.user.mention)

        if settings.get("tag_founder") and founder:
            mention_text += f"👑 Founder:\n{founder}\n\n"

        if settings.get("tag_admins") and admins:
            mention_text += "🔔 Admins:\n" + " ".join(admins[:5]) + "\n\n"

    except Exception:
        pass

    return mention_text


@app.on_message(filters.command(["report", "admin"]) & filters.group)
async def report_handler(client, message: Message):

    chat_id = message.chat.id
    user = message.from_user

    settings = await get_settings(chat_id)

    # System disabled
    if not settings.get("status", True):
        return await message.reply("⚠️ Report system is disabled in this group.")

    # Block admins from using
    try:
        member = await client.get_chat_member(chat_id, user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("❌ Admins cannot use this command.")
    except UserNotParticipant:
        return

    staff_group = settings.get("staff_group")
    if not staff_group:
        return await message.reply("⚠️ Staff group is not configured.")

    # Determine reported message
    if message.reply_to_message:
        reported_text = (
            message.reply_to_message.text
            or message.reply_to_message.caption
            or "📎 Media Message"
        )
    else:
        reported_text = message.text

    mention_text = await get_admin_mentions(client, chat_id, settings)

    text = build_report_text(
        user=user,
        chat_title=message.chat.title,
        reported_text=reported_text,
        mention_text=mention_text
    )

    # Jump Button
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📍 Jump to Message",
                    url=message.link
                )
            ]
        ]
    )

    # Forward original message (if replying)
    if message.reply_to_message:
        try:
            await client.forward_messages(
                staff_group,
                chat_id,
                message.reply_to_message.id
            )
        except Exception:
            pass

    await client.send_message(
        staff_group,
        text,
        reply_markup=button,
        disable_web_page_preview=True
    )

    await message.reply("✅ Report sent to staff successfully.")
