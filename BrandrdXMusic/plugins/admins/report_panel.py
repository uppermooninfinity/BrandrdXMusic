# plugins/admin/report_panel.py

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ChatMemberStatus

from yourbot import app  # change this
from BrandrdXMusic.mongo.report_db import get_settings


def build_panel_text(settings):
    status = "🟢 Enabled" if settings.get("status", True) else "🔴 Disabled"
    staff = settings.get("staff_group")

    staff_text = f"`{staff}`" if staff else "Not Set"

    tag_admins = "✅" if settings.get("tag_admins", True) else "❌"
    tag_founder = "✅" if settings.get("tag_founder", True) else "❌"

    return (
        f"⚙ **Admin Report Settings Panel**\n\n"
        f"📡 System Status: {status}\n"
        f"👥 Staff Group: {staff_text}\n\n"
        f"🔔 Tag Admins: {tag_admins}\n"
        f"👑 Tag Founder: {tag_founder}\n"
    )


def build_panel_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Toggle System", callback_data="rp_toggle")
            ],
            [
                InlineKeyboardButton("👥 Set Staff Group", callback_data="rp_set_staff")
            ],
            [
                InlineKeyboardButton("🔔 Toggle Admin Tags", callback_data="rp_toggle_admins")
            ],
            [
                InlineKeyboardButton("👑 Toggle Founder Tag", callback_data="rp_toggle_founder")
            ]
        ]
    )


@app.on_message(filters.command("reportpanel") & filters.group)
async def report_panel(client, message: Message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Only admins can open panel
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return

    settings = await get_settings(chat_id)

    text = build_panel_text(settings)

    await message.reply(
        text,
        reply_markup=build_panel_buttons()
    )
