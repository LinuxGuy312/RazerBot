import asyncio
from Razerbot.events import register
from Razerbot.modules.sql.mute_sql import *
from Razerbot import pbot, EVENT_LOGS, LOGGER, OWNER_ID
from pyrogram.enums import *

EVENT_LOGGER = True

@register(incoming=True, pattern="(?:\s|$)([\s\S]*)")
async def watcher(bot, m):
    if is_muted(m.from_user.id, m.chat_id):
        await m.delete()


@register(pattern="[./!]delmute(?:\s|$)([\s\S]*)")
async def delmute(bot, m):
    jadu = m.pattern_match.group(1)
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat_id, userid)
    myid = (await pbot.get_me()).id
    if not ((mem.status == ChatMemberStatus.ADMINISTRATOR) or (userid == OWNER_ID)):
        return await m.reply("This command is only for admins.")
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply("How can you be so noob? :/")
    stat = await pbot.get_chat_member(m.chat.id, myid)
    if stat.status not in [ChatMemeberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await m.reply("`I can't mute a person without having admin rights` ಥ﹏ಥ")
    user, reason = m.reply_to_message.from_user or await pbot.get_users(jadu)
    if not user:
        return
    if user.id == myid:
        return await m.reply("Sorry, I can't mute myself.")
    if user.id == userid:
        return await m.reply("Trying to mute yourself? Not gonna happen")
    if user.id == OWNER_ID:
        return await m.reply("Nice Try Muting my owner right there XD")
    if is_muted(user.id, m.chat.id):
        return await m.reply("This user is already muted in this chat ~~lmfao sed rip~~")
    try:
        if not mem.permissions.can_send_messages:
            return await m.reply("This user is already muted in this chat ~~lmfao sed rip~~")
    except AttributeError:
        pass
    except Exception as e:
        return await m.reply(f"**Error : **`{e}`")
    unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
    if "privileges" in vars(stat) and vars(stat)["privileges"] is not None:
        if stat.privileges.can_delete_messages is not True:
            return await m.reply("`I can't mute a person if I dont have delete messages permission. ಥ﹏ಥ`")
    elif vars(stat)["privileges"] is None:
        return await m.reply("`I can't mute a person without having admin rights.` ಥ﹏ಥ")
    mute(user.id, m.chat.id)
    if reason:
        await map(func, iter1).reply(
            f"[{user.first_name}]({unid}) is muted in {m.chat.title}\n"
            f"Reason: `{reason}`"
        )
    else:
        await m.reply(f"[{user.first_name}]({unid}) is muted in {m.chat.title}")
    if EVENT_LOGGER:
        await pbot.send_message(
            EVENT_LOGS,
            "#MUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {m.chat.title}(`{m.chat.id}`)",
        )

@register(pattern="[./!]undelmute(?:\s|$)([\s\S]*)")
async def undelmute(bot, m):
    jadu = m.pattern_match.group(1)
    userid = m.from_user.id
    mem = await pbot.get_chat_member(m.chat_id, userid)
    if not ((mem.status == ChatMemberStatus.ADMINISTRATOR) or (userid == OWNER_ID)):
        return await m.reply("This command is only for admins.")
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply("How can you be so noob? :/")
    user = m.reply_to_message.from_user or await pbot.get_users(jadu)
    if not user:
        return
    try:
        unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
        if is_muted(user.id, m.chat_id):
            unmute(user.id, m.chat_id)
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