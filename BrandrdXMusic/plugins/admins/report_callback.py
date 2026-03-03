# plugins/admin/report_callbacks.py

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

from yourbot import app  # change this
from BrandrdXMusic.mongo.report_db import (
    get_settings,
    update_setting,
    toggle_system,
    set_staff_group
)


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
            [InlineKeyboardButton("🔄 Toggle System", callback_data="rp_toggle")],
            [InlineKeyboardButton("👥 Set Staff Group (Use in staff group)", callback_data="rp_set_staff")],
            [InlineKeyboardButton("🔔 Toggle Admin Tags", callback_data="rp_toggle_admins")],
            [InlineKeyboardButton("👑 Toggle Founder Tag", callback_data="rp_toggle_founder")]
        ]
    )


async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


@app.on_callback_query(filters.regex("^rp_"))
async def report_callbacks(client, query: CallbackQuery):

    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await query.answer("Only admins can use this.", show_alert=True)

    settings = await get_settings(chat_id)

    data = query.data

    # Toggle System
    if data == "rp_toggle":
        new_status = await toggle_system(chat_id)
        await query.answer(f"System {'Enabled' if new_status else 'Disabled'}")

    # Toggle Admin Tag
    elif data == "rp_toggle_admins":
        current = settings.get("tag_admins", True)
        await update_setting(chat_id, "tag_admins", not current)
        await query.answer("Admin tagging updated")

    # Toggle Founder Tag
    elif data == "rp_toggle_founder":
        current = settings.get("tag_founder", True)
        await update_setting(chat_id, "tag_founder", not current)
        await query.answer("Founder tagging updated")

    # Set Staff Group
    elif data == "rp_set_staff":

        # IMPORTANT:
        # Admin must press this inside the STAFF GROUP
        # So chat_id becomes staff group id

        await set_staff_group(chat_id, chat_id)
        await query.answer("Staff group set successfully")

    # Refresh panel
    new_settings = await get_settings(chat_id)

    await query.message.edit_text(
        build_panel_text(new_settings),
        reply_markup=build_panel_buttons()
    )
