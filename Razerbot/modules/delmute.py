import asyncio
from Razerbot.modules.sql.mute_sql import *
from Razerbot import pbot, EVENT_LOGS, LOGGER, BOT_ID, OWNER_ID

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram import filters

EVENT_LOGGER = True


@pbot.on_message(group=69)
async def watcher(_, m):
    if is_muted(m.from_user.id, m.chat.id):
        await m.delete()


@pbot.on_message(filters.command("delmute", prefixes=["/", ".", "!"]))
async def delmute(_, m):
    if not m.from_user:
        return
    if m.chat.type == ChatType.PRIVATE:
        return
    try:
        if m.reply_to_message:
            jadu = m.reply_to_message.from_user.id
        else:
            jadu = m.text.split()[1]
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat.id, userid)
    if not ((mem.status == ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER) or (userid == OWNER_ID)):
        return await m.reply_text("This command is only for admins.")
    stat = await pbot.get_chat_member(m.chat.id, BOT_ID)
    if stat.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await m.reply_text("`I can't mute a person without having admin rights` ಥ﹏ಥ")
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
    await m.reply_text(f"{user.mention} [`{user.id}`] is now muted in {m.chat.title} by {m.from_user.mention}.")
    if EVENT_LOGGER:
        await pbot.send_message(
            EVENT_LOGS,
            "#DEL-MUTED\n"
            f"**User :** {user.mention} with id `{user.id}`\n"
            f"**Chat :** {m.chat.title}(`{m.chat.id}`)",
        )

@pbot.on_message(filters.command("undelmute", prefixes=["/", ".", "!"]))
async def undelmute(_, m):
    try:
        jadu = m.text.split(" ")[1]
    except IndexError:
        jadu = None
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat.id, userid)
    if not ((mem.status == ChatMemberStatus.ADMINISTRATOR) or (userid == OWNER_ID)):
        return await m.reply("This command is only for admins.")
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply("How can you be so noob? :/")
    try:
        user = m.reply_to_message.from_user
    except AttributeError:
        user = await pbot.get_users(jadu)
    except Exception as e:
        return await m.reply(f"Error : {e}")
    if not user:
        return
    try:
        unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
        if is_muted(user.id, m.chat.id):
            unmute(user.id, m.chat.id)
            await m.reply(f"[{user.first_name}]({unid}) is unmuted in {m.chat.title}")
        else:
            return await m.reply("`This user can already speak freely in this chat`")
    except Exception as e:
        return await m.reply(f"**Error : **`{e}`")
    if EVENT_LOGGER:
        await pbot.send_message(
            EVENT_LOGS,
            "#UNMUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {m.chat.title}(`{m.chat.id}`)"
        )

__mod_name__ = "Delmute"
__help__ = """Delmute

Usage:
> /delmute <reply to anyone> or <user id>
> /undelmute <reply to muted user> or <user id>

Will delete any incoming message from the muted user (even admin)."""
