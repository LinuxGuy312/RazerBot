from platform import python_version as y
from telegram import __version__ as o
from pyrogram import __version__ as z
from telethon import __version__ as s
from telethon import Button
from Razerbot import telethn, SUPPORT_CHAT, BOT_NAME, OWNER_USERNAME
from Razerbot.events import register

@register(pattern="^[./!]alive")
async def alive(event):
    ALIVE_PIC = "https://graph.org/file/36c17c0f22aeea9c99895.jpg"
    ALIVE_TEXT = f"""
Hᴇʟʟᴏ {event.sender.first_name}!
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
    buttons = [
        Button.url("sᴜᴘᴘᴏʀᴛ", f"https://t.me/{SUPPORT_CHAT}"),
        Button.url("ᴏᴡɴᴇʀ", f"https://t.me/{OWNER_USERNAME}")
    ]
    await telethn.send_file(
        event.chat_id,
        ALIVE_PIC,
        caption=ALIVE_TEXT,
        reply_to=event.sender.id,
        buttons=buttons
    )