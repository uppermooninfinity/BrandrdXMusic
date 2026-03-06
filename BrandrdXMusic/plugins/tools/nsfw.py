from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.mongo import db

nsfw_media = mongodb.nsfw_media
nsfw_stickers = mongodb.nsfw_stickers


# ───────────────────────
# mark media nsfw
# ───────────────────────
@app.on_message(filters.command(["marknsfw"], prefixes=["/"]) & filters.reply)
async def mark_nsfw(_, message: Message):

    if message.from_user.id not in app.owner and message.from_user.id not in app.sudoers:
        return await message.reply_text("» ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏʀ ꜱᴜᴅᴏᴇʀꜱ.")

    reply = message.reply_to_message

    file_id = None

    if reply.photo:
        file_id = reply.photo.file_id

    elif reply.video:
        file_id = reply.video.file_id

    elif reply.sticker:
        file_id = reply.sticker.file_id

    if not file_id:
        return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ.")

    await nsfw_media.update_one(
        {"file_id": file_id},
        {"$set": {"file_id": file_id}},
        upsert=True,
    )

    await message.reply_text(
        "⚠️ ɴꜱꜰᴡ ᴍᴀʀᴋᴇᴅ.\n\n"
        "❝ ɢʀᴏᴜᴘ ꜱᴀꜰᴇᴛʏ ᴍᴀᴛᴛᴇʀꜱ ❞\n"
        "❝ ʀᴇꜱᴘᴇᴄᴛ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ ❞"
    )


# ───────────────────────
# mark sticker pack nsfw
# ───────────────────────
@app.on_message(filters.command(["marksticknsfw"], prefixes=["/"]) & filters.reply)
async def mark_stick_pack(_, message: Message):

    if message.from_user.id not in app.owner and message.from_user.id not in app.sudoers:
        return await message.reply_text("» ᴏɴʟʏ ᴏᴡɴᴇʀ ᴏʀ ꜱᴜᴅᴏᴇʀꜱ.")

    reply = message.reply_to_message

    if not reply.sticker:
        return await message.reply_text("» ʀᴇᴘʟʏ ᴛᴏ ꜱᴛɪᴄᴋᴇʀ.")

    pack = reply.sticker.set_name

    await nsfw_stickers.update_one(
        {"pack": pack},
        {"$set": {"pack": pack}},
        upsert=True,
    )

    await message.reply_text(
        "🚫 ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ʙʟᴏᴄᴋᴇᴅ.\n\n"
        "❝ ɴꜱꜰᴡ ᴄᴏɴᴛᴇɴᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ❞"
    )


# ───────────────────────
# detect nsfw media
# ───────────────────────
@app.on_message(filters.group)
async def detect_nsfw(_, message: Message):

    file_id = None

    if message.photo:
        file_id = message.photo.file_id

    elif message.video:
        file_id = message.video.file_id

    elif message.sticker:
        file_id = message.sticker.file_id

    if not file_id:
        return

    data = await nsfw_media.find_one({"file_id": file_id})

    if data:
        try:
            await message.delete()
        except:
            return

        warn = await message.reply_text(
            "⚠️ ɴꜱꜰᴡ ᴄᴏɴᴛᴇɴᴛ ʙʟᴏᴄᴋᴇᴅ.\n"
            "❝ ᴋᴇᴇᴘ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ❞"
        )

        await warn.delete()


# ───────────────────────
# detect nsfw sticker pack
# ───────────────────────
@app.on_message(filters.group & filters.sticker)
async def detect_pack(_, message: Message):

    pack = message.sticker.set_name

    data = await nsfw_stickers.find_one({"pack": pack})

    if data:
        try:
            await message.delete()
        except:
            return

        warn = await message.reply_text(
            "⚠️ ɴꜱꜰᴡ ꜱᴛɪᴄᴋᴇʀ ʙʟᴏᴄᴋᴇᴅ.\n"
            "❝ ʀᴇꜱᴘᴇᴄᴛ ɢʀᴏᴜᴘ ʀᴜʟᴇꜱ ❞"
        )

        await warn.delete()
