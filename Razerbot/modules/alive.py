from platform import python_version as pyver
from telegram import __version__ as libver
from pyrogram import __version__ as pyrover
from telethon import __version__ as telthnver
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Razerbot import pbot, SUPPORT_CHAT, BOT_NAME, OWNER_ID, OWNER_USERNAME, ALIVE_IMG

@pbot.on_message(filters.command("alive", prefixes=["/", ".", "!"]))
async def alive(_, message):
    ALIVE_TEXT = f"""
Hᴇʟʟᴏ {message.from_user.mention}!
───────────────────────
× I'ᴍ {BOT_NAME}, A Pᴏᴡᴇʀꜰᴜʟ Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ.
× I'ᴍ Aʟɪᴠᴇ ᴀɴᴅ Wᴏʀᴋɪɴɢ Hᴀʀᴅ!!
───────────────────────
× Oᴡɴᴇʀ : @{OWNER_USERNAME}
× Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ : `{pyver()}`
× Lɪʙʀᴀʀʏ Vᴇʀsɪᴏɴ : `{libver}`
× Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ : `{telthnver}`
× Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ : `{pyrover}`
───────────────────────"""
    buttons = [
                [
                    InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"), 
                    InlineKeyboardButton(text="oᴡɴᴇʀ", user_id=OWNER_ID)
                ]
            ]
        
    await message.reply_photo(
        photo=ALIVE_IMG,
        caption=ALIVE_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )