import asyncio
from Razerbot.modules.sql.mute_sql import *
from Razerbot import pbot, EVENT_LOGS, LOGGER, BOT_ID, OWNER_ID

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram import filters

EVENT_LOGGER = True

DMUTE = []

@pbot.on_message(group=7)
async def watcher(_, m):
    if not m.from_user:
        return
    if is_muted(m.from_user.id, m.chat.id):
        await m.delete()


@pbot.on_message(filters.command("delmute", prefixes=["/", ".", "!"]))
async def delmute(_, m):
    if not m.from_user:
        return
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply_text("How can you be so noob? :/")
    try:
        if m.reply_to_message:
            jadu = m.reply_to_message.from_user.id
            lst = m.text.split(" ")[1:]
            reason = " ".join(lst)
        else:
            jadu = m.text.split(" ")[1]
            lst = m.text.split(" ")[2:]
            reason = " ".join(lst)
    except Exception as e:
        return await m.reply_text(f"**Error:** {e}")
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat.id, userid)
    if not ((mem.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]) or (userid == OWNER_ID)):
        return await m.reply_text("This command is only for admins.")
    stat = await pbot.get_chat_member(m.chat.id, BOT_ID)
    if stat.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await m.reply_text("`I can't mute a person without having admin rights` ಥ﹏ಥ")
    if "privileges" in vars(stat) and vars(stat)["privileges"] is not None:
        if stat.privileges.can_delete_messages is False:
            return await m.reply_text("`I can't mute a person if I dont have delete messages permission. ಥ﹏ಥ`")
    try:
        user = await pbot.get_users(jadu)
    except:
        return
    if user.id == BOT_ID:
        return await m.reply_text("Sorry, I can't mute myself.")
    if user.id == userid:
        return await m.reply_text("Trying to mute yourself? Not gonna happen")
    if user.id == OWNER_ID:
        return await m.reply_text("Nice Try Muting my owner right there XD")
    if is_muted(user.id, m.chat.id):
        return await m.reply_text("This user is already muted in this chat ~~lmfao sed rip~~")
    try:
        if not mem.permissions.can_send_messages:
            return await m.reply_text("This user is already muted in this chat ~~lmfao sed rip~~")
    except AttributeError:
        pass
    except Exception as e:
        return await m.reply_text(f"**Error : **`{e}`")
    mute(user.id, m.chat.id)
    if reason == '':
        msg =  f"{user.mention} [`{user.id}`] is now muted in {m.chat.title} by {m.from_user.mention}."
        evt_msg = f"#MUTED\n**User :** {user.mention} with id `{user.id}`\n**Chat :** {m.chat.title}(`{m.chat.id}`)"
    else:
        msg = f"{user.mention} [`{user.id}`] is now muted in {m.chat.title} by {m.from_user.mention}.\nReason: `{reason}`"
        evt_msg = f"#MUTED\n**User :** {user.mention} with id `{user.id}`\n**Chat :** {m.chat.title}(`{m.chat.id}`)\n**Reason :** `{reason}`"
    await m.reply_text(msg) 
    if EVENT_LOGGER:
        await pbot.send_message(EVENT_LOGS, evt_msg)

@pbot.on_message(filters.command(["undelmute", "delunmute"], prefixes=["/", ".", "!"]))
async def undelmute(_, m):
    if not m.from_user:
        return
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply_text("How can you be so noob? :/")
    try:
        if m.reply_to_message:
            jadu = m.reply_to_message.from_user.id
        else:
            jadu = m.text.split(" ")[1]
    except Exception as e:
        return await m.reply_text(f"**Error:** {e}")
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat.id, userid)
    if not ((mem.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]) or (userid == OWNER_ID)):
        return await m.reply_text("This command is only for admins.")
    try:
        user = await pbot.get_users(jadu)
    except:
        return
    if user.id == BOT_ID:
        return await m.reply_text("I am the one who mutes lol XD")
    if user.id == userid:
        return await m.reply_text("Hey! You can't unmute yourself! That's cheating XD")
    if user.id == OWNER_ID:
        return await m.reply_text("How can I unmute my owner when I can't even mute him LOL XD")
    try:
        if is_muted(user.id, m.chat.id):
            unmute(user.id, m.chat.id)
            await m.reply(f"{user.mention} [`{user.id}`] is unmuted in {m.chat.title} by {m.from_user.mention}")
        else:
            return await m.reply("`This user can already speak freely in this chat`")
    except Exception as e:
        return await m.reply(f"**Error : **`{e}`")
    if EVENT_LOGGER:
        await pbot.send_message(
            EVENT_LOGS,
            "#UNMUTED\n"
            f"**User :** {user.mention} with id `{user.id}`\n"
            f"**Chat :** {m.chat.title}(`{m.chat.id}`)"
        )

__mod_name__ = "Dᴇʟᴍᴜᴛᴇ"
__help__ = """Dᴇʟᴍᴜᴛᴇ

Usage:
> /delmute <reply to anyone> or <user id>
> /undelmute <reply to muted user> or <user id>

Will delete any incoming message from the muted user (even admin)."""
