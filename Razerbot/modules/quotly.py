from io import BytesIO
from traceback import format_exc

from pyrogram import filters
from pyrogram.types import Message

from Razerbot import pbot as app, arq
from Razerbot.utils.errors import capture_err

__mod_name__ = "Qᴜᴏᴛʟʏ"
__help__ = """
/q - To quote a message.
/q [INTEGER] - To quote more than 1 messages.
/q r - to quote a message with it's reply

Use .q to quote using userbot
"""


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> list:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]

@app.on_message(filters.command("q") & ~filters.private & ~filters.edited)
@capture_err
async def quotly_func(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ǫᴜᴏᴛᴇ ɪᴛ.")
    if not message.reply_to_message.text:
        return await message.reply_text(
            "ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ʜᴀs ɴᴏ ᴛᴇxᴛ, ᴄᴀɴ'ᴛ ǫᴜᴏᴛᴇ ɪᴛ."
        )
    m = await message.reply_text("ǫᴜᴏᴛɪɴɢ ᴍᴇssᴀɢᴇs...")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("ᴀʀɢᴜᴍᴇɴᴛ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 2-10.")

            count = arg[1]

            # Fetching 5 extra messages so tha twe can ignore media
            # messages and still end up with correct offset
            messages = [
                i
                for i in await client.get_messages(
                    message.chat.id,
                    range(
                        message.reply_to_message.message_id,
                        message.reply_to_message.message_id + (count + 5),
                    ),
                    replies=0,
                )
                if not i.empty and not i.media
            ]
            messages = messages[:count]
        else:
            if getArg(message) != "r":
                return await m.edit(
                    "ɪɴᴄᴏʀʀᴇᴄᴛ ᴀʀɢᴜᴍᴇɴᴛ, ᴘᴀss 'r' ᴏʀ <int>, ᴇx: /q 2"
                )
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.message_id,
                replies=1,
            )
            messages = [reply_message]
    else:
        return await m.edit(
            "ɪɴᴄᴏʀʀᴇᴄᴛ ᴀʀɢᴜᴍᴇɴᴛ, ᴄʜᴇᴄᴋ ǫᴜᴏᴛʟʏ ᴍᴏᴅᴜʟᴇ ɪɴ ʜᴇʟᴘ sᴇᴄᴛɪᴏɴ."
        )
    try:
        if not message:
            return await m.edit("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.")

        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ǫᴜᴏᴛɪɴɢ ᴍᴇssᴀɢᴇs,"
            + " ᴛʜɪs ᴇʀʀᴏʀ ᴜsᴜᴀʟʟʏ ʜᴀᴘᴘᴇɴs ᴡʜᴇɴ ᴛʜᴇʀᴇ's ᴀ"
            + " ᴍᴇssᴀɢᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ sᴏᴍᴇᴛʜɪɴɢ ᴏᴛʜᴇʀ ᴛʜᴀɴ ᴛᴇxᴛ,"
            + " ᴏʀ ᴏɴᴇ ᴏꜰ ᴛʜᴇ ᴍᴇssᴀɢᴇs ɪɴ-ʙᴇᴛᴡᴇᴇɴ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ."
        )
        e = format_exc()
        print(e)
