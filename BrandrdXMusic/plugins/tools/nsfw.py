import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    enable_nsfw,
    disable_nsfw,
    is_nsfw_enabled,
    add_nsfw_media,
    remove_nsfw_media,
    is_nsfw_media,
    add_nsfw_pack,
    remove_nsfw_pack,
    is_nsfw_pack,
    nsfw_stats
)

# ================= CONFIG ================= #

NSFW_LOGS = -1001234567890  # change to your log channel


# ================= ADMIN CHECK ================= #

async def is_admin(chat_id, user_id):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    )


# ================= ENABLE / DISABLE ================= #

@app.on_message(filters.command("antinsfw", prefixes=["/"]) & filters.group)
async def toggle_nsfw(_, message: Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("admins only.")

    if len(message.command) < 2:
        return await message.reply("/antinsfw on | off")

    state = message.command[1].lower()

    if state == "on":
        await enable_nsfw(message.chat.id)
        await message.reply("nsfw protection enabled.")

    elif state == "off":
        await disable_nsfw(message.chat.id)
        await message.reply("nsfw protection disabled.")


# ================= MARK MEDIA ================= #

@app.on_message(filters.command("marknsfw", prefixes=["/"]) & filters.reply)
async def mark_nsfw(_, message: Message):

    if message.from_user.id not in app.owner_ids:
        return

    media = message.reply_to_message

    file_id = (
        media.photo.file_unique_id if media.photo else
        media.video.file_unique_id if media.video else
        media.sticker.file_unique_id if media.sticker else None
    )

    if not file_id:
        return await message.reply("reply to photo/video/sticker.")

    await add_nsfw_media(file_id)

    await message.reply("media marked nsfw.")


# ================= MARK STICKER PACK ================= #

@app.on_message(filters.command("marksticknsfw", prefixes=["/"]) & filters.reply)
async def mark_pack(_, message: Message):

    if message.from_user.id not in app.owner_ids:
        return

    if not message.reply_to_message.sticker:
        return await message.reply("reply to sticker.")

    pack = message.reply_to_message.sticker.set_name

    await add_nsfw_pack(pack)

    await message.reply("sticker pack blocked.")


# ================= REMOVE NSFW ================= #

@app.on_message(filters.command("remark", prefixes=["/"]) & filters.reply)
async def remark(_, message: Message):

    if message.from_user.id not in app.owner_ids:
        return

    media = message.reply_to_message

    file_id = (
        media.photo.file_unique_id if media.photo else
        media.video.file_unique_id if media.video else
        media.sticker.file_unique_id if media.sticker else None
    )

    if not file_id:
        return

    await remove_nsfw_media(file_id)

    if media.sticker:
        await remove_nsfw_pack(media.sticker.set_name)

    await message.reply("nsfw removed.")


# ================= DATABASE SCAN ================= #

@app.on_message(filters.command("nsfwscan", prefixes=["/"]))
async def scan(_, message: Message):

    media, packs = await nsfw_stats()

    text = (
        "nsfw database\n\n"
        f"blocked media : {media}\n"
        f"blocked packs : {packs}"
    )

    await message.reply(text)


# ================= DETECT NSFW ================= #

@app.on_message(filters.group & (filters.photo | filters.video | filters.sticker))
async def detect(_, message: Message):

    enabled = await is_nsfw_enabled(message.chat.id)

    if not enabled:
        return

    file_id = (
        message.photo.file_unique_id if message.photo else
        message.video.file_unique_id if message.video else
        message.sticker.file_unique_id if message.sticker else None
    )

    pack = message.sticker.set_name if message.sticker else None

    if not file_id:
        return

    media_match = await is_nsfw_media(file_id)
    pack_match = await is_nsfw_pack(pack) if pack else False

    if not media_match and not pack_match:
        return

    try:
        await message.delete()
    except:
        return

    warn = await message.reply(
        f"{message.from_user.mention} nsfw content blocked."
    )

    await asyncio.sleep(4)

    try:
        await warn.delete()
    except:
        pass

    # ================= LOG ================= #

    try:

        log_text = (
            "nsfw blocked\n\n"
            f"chat : {message.chat.title}\n"
            f"user : {message.from_user.mention}\n"
            f"id : `{message.from_user.id}`"
        )

        await app.send_message(NSFW_LOGS, log_text)

    except:
        pass
