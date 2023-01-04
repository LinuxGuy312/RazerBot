from pyrogram.types import Message
from pyrogram import filters
from Razerbot import pbot as app, aiohttpsession as aiosession
from Razerbot.utils.errors import capture_err
from asyncio import gather
from io import BytesIO


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@app.on_message(filters.command("carbon"))
async def carbon_func(_, message):
    try:
        cod = message.reply_to_message.text
    except:
        cod = message.text.split(" ", 1)[1]
    m = await message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...")
    carbon = await make_carbon(cod)
    await m.edit("ᴜᴩʟᴏᴀᴅɪɴɢ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ...")
    await app.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()

__mod_name__ = "Cᴀʀʙᴏɴ"

__help__ = """
Generate a carbon of given text 

 ❍ /carbon <text>
"""