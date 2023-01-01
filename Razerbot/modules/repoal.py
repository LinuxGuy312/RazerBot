from platform import python_version as y
from telegram import __version__ as o
from pyrogram import __version__ as z
from telethon import __version__ as s
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from Razerbot import pbot, START_IMG, SUPPORT_CHAT, BOT_NAME, OWNER_USERNAME


@pbot.on_message(filters.command("repo"))
async def repo(_, message):
    await message.reply_photo(
        photo=START_IMG,
        caption=f"""ʜᴇʏ ɪ'ᴍ {BOT_NAME}

⥤ ᴏᴡɴᴇʀ : @{OWNER_USERNAME}
⥤ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : `{y()}`
⥤ ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ : `{o}`
⥤ ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : `{s}`
⥤ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : `{z}`

ʀᴀᴢᴇʀʙᴏᴛ ɪs ᴀɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ ʙᴏᴛ ᴘʀᴏᴊᴇᴄᴛ.
ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ.
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", url="https://github.com/LinuxGuy312/RazerBot"), 
                    InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")
                ]
            ]
        )
    )


@pbot.on_message(filters.command("alive"))
async def repo(_, message):
    ALIVE_PIC = "https://graph.org/file/36c17c0f22aeea9c99895.jpg"
    ALIVE_TEXT = f"""
Hᴇʟʟᴏ {message.sender.first_name}!
───────────────────────
× I'ᴍ {BOT_NAME}, A Pᴏᴡᴇʀꜰᴜʟ Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ.
× I'ᴍ Aʟɪᴠᴇ ᴀɴᴅ Wᴏʀᴋɪɴɢ Hᴀʀᴅ!!
───────────────────────
× Oᴡɴᴇʀ : @{OWNER_USERNAME}
× Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ : `{y()}`
× Lɪʙʀᴀʀʏ Vᴇʀsɪᴏɴ : `{o}`
× Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ : `{s}`
× Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ : `{z}`
───────────────────────"""

    await message.reply_photo(
        photo=ALIVE_PIC,
        caption=ALIVE_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"), 
                    InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")
                ]
            ]
        )
    )