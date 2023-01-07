from pyrogram import filters
from Razerbot import LOGGER, pbot


DMUTED = []
msgs = []

@pbot.on_message(filters.command("delmutem"))
async def delmute(bot, m):
    res = "Unknown error occurred"
    try:
        uid = m.reply_to_message.from_user.id
    except Exception:
        uid = 0000
    t_uid = m.text[len("/delmutem ") :] if m.text[len("/delmutem ") :] !="" else 0000
    if uid == bot.me.id or int(t_uid) == bot.me.id:
        return await m.reply("Noob! Why would I mute myself?")
    if t_uid and not uid:
        DMUTED.append(int(t_uid))
        res = f"Del muted {t_uid}"
    else:
        DMUTED.append(int(uid))
        res = f"Del muted {uid}"
    await m.reply(res)

@pbot.on_message(filters.command("undelmutem"))
async def undelmute(bot, m):
    res = "Unknown error occurred"
    try:
        uid = m.reply_to_message.from_user.id
    except Exception:
        uid = 0000
    t_uid = m.text[len("/undelmutem ") :]
    try:
        if t_uid and not uid:
            DMUTED.remove(int(t_uid))
            res = "Successfully undelmuted!"
        else:
            DMUTED.remove(int(uid))
            res = "Successfully undelmuted!"
    except Exception as e:
        res = e
    await m.reply(res)

@pbot.on_message(filters.command("delmuted"))
async def listdmited(bot, m):
    await m.reply(f"List of delmuted users:", *DMUTED, sep="\n")


limit = [0]
@pbot.on_message(group=1)
async def delmsg(bot, m):
    if len(DMUTED)==0:
        return 
    if m.from_user.id in DMUTED:
         await m.delete()
         limit.insert(0, limit[0]+1)
         if limit[0] < 5:
             if len(msgs)!=0:
                 await msgs[-1].delete()
                 msgs.remove(msgs[-1])
             y = (await bot.send_message(text=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id}) You were del muted due to spam if this is a mistake kindly contact admins.", chat_id=m.chat.id))
             y
             msgs.append(y)
 
__mod_name__ = "Delete-mute"
__help__ = """It's a type of painful mute, when used on user their messages will be instantly deleted.

/delmute user_id or reply to user's message
- can del mute another admin too

/undelmute - to undelmute a user.
/delmuted - list of del muted user's
"""
