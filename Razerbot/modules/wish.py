from random import uniform
from Razerbot import pbot
from pyrogram import filters

@pbot.on_edited_message(filters.command('wish'))
@pbot.on_message(filters.command('wish'))
async def wish(bot, event):
    chance = str(uniform(0,100))[0:5]
    msg = f"**Your wish has been cast.** ✨\n\n__Chances of Success: {chance}%__"
    await event.reply(msg)

__mod_name__ = "Wɪsʜ"
__help__ = """Wɪsʜ

Usage:
> /wish <your wish>

You can cast a wish and it'll tell chance of its success."""