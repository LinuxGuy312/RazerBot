import asyncio
from Razerbot.events import register
from Razerbot.modules.sql.mute_sql import *
from Razerbot import telethn as tbot, pbot, EVENT_LOGS, LOGGER, OWNER_ID
from telethon.tl.types import MessageEntityMentionName
from telethon import events

EVENT_LOGGER = True

@pbot.on_message(group=1)
async def watcher(_, m):
    if is_muted(m.from_user.id, m.chat.id):
        await m.delete()


async def get_user_from_event(
    event,
    razevent=None,
    secondgroup=None,
    thirdgroup=None,
    nogroup=False,
    noedits=False,
):
    if razevent is None:
        razevent = event
    if nogroup is False:
        if secondgroup:
            args = event.pattern_match.group(2).split(" ", 1)
        elif thirdgroup:
            args = event.pattern_match.group(3).split(" ", 1)
        else:
            args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    try:
        if args:
            user = args[0]
            if len(args) > 1:
                extra = "".join(args[1:])
            if user.isnumeric() or (user.startswith("-") and user[1:].isnumeric()):
                user = int(user)
            if event.message.entities:
                probable_user_mention_entity = event.message.entities[0]
                if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                    user_id = probable_user_mention_entity.user_id
                    user_obj = await tbot.get_entity(user_id)
                    return user_obj, extra
            if isinstance(user, int) or user.startswith("@"):
                user_obj = await tbot.get_entity(user)
                return user_obj, extra
    except Exception as e:
        LOGGER.error(str(e))
    try:
        if nogroup is False:
            if secondgroup:
                extra = event.pattern_match.group(2)
            else:
                extra = event.pattern_match.group(1)
        if event.is_private:
            user_obj = await event.get_chat()
            return user_obj, extra
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            if previous_message.from_id is None:
                if not noedits:
                    await edit_delete(razevent, "`Well that's an anonymous admin !`")
                return None, None
            user_obj = await event.client.get_entity(previous_message.sender_id)
            return user_obj, extra
        if not args:
            if not noedits:
                await razevent.edit("`Pass the user's username, id or reply!`")
                await asyncio.sleep(5)
                await razevent.delete()
            return None, None
    except Exception as e:
        LOGGER.error(str(e))
    if not noedits:
        await razevent.edit("__Couldn't fetch user to proceed further.__")
        await asyncio.sleep(5)
        await razevent.delete()
    return None, None


@register(pattern="^[!/]delmute(?:\s|$)([\s\S]*)")
async def delmute(event):
    userid = event.sender.id
    perm = await tbot.get_permissions(event.chat_id, userid)
    if not (perm.is_admin or userid == OWNER_ID):
        return await event.reply("This command is only for admins.")
    if event.is_private:
        return await event.reply("How can you be so noob? :/")
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await event.reply("`I can't mute a person without having admin rights` ಥ﹏ಥ")
    user, reason = await get_user_from_event(event)
    myid = (await tbot.get_me()).id
    if not user:
        return
    if user.id == myid:
        return await event.reply("Sorry, I can't mute myself.")
    if user.id == userid:
        return await event.reply("Trying to mute yourself? Not gonna happen")
    if user.id == OWNER_ID:
        return await event.reply("Nice Try Muting my owner right there XD")
    if is_muted(user.id, event.chat_id):
        return await event.reply("`This user is already muted in this chat ~~lmfao sed rip~~`")
    result = await tbot.get_permissions(event.chat_id, user.id)
    try:
        if result.participant.banned_rights.send_messages:
            return await event.reply("`This user is already muted in this chat ~~lmfao sed rip~~`")
    except AttributeError:
        pass
    except Exception as e:
        return await event.reply(f"**Error : **`{e}`")
    unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is not True:
            return await event.reply("`I can't mute a person if I dont have delete messages permission. ಥ﹏ಥ`")
    elif "creator" not in vars(chat):
        return await event.reply("`I can't mute a person without having admin rights.` ಥ﹏ಥ  ")
    mute(user.id, event.chat_id)
    if reason:
        await event.reply(
            f"[{user.first_name}]({unid}) is muted in {event.chat.title}\n"
            f"Reason: {reason}`"
        )
    else:
        await event.reply(f"[{user.first_name}]({unid}) is muted in {event.chat.title}")
    if EVENT_LOGGER:
        await tbot.send_message(
            EVENT_LOGS,
            "#MUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {event.chat.title}(`{event.chat_id}`)",
        )

@register(pattern="^[!/]undelmute(?:\s|$)([\s\S]*)")
async def undelmute(event):
    userid = event.sender.id
    perm = await tbot.get_permissions(event.chat_id, userid) 
    if not (perm.is_admin or userid == OWNER_ID):
        return await event.reply("This command is only for admins.")
    if event.is_private:
        return await event.reply("How can you be so noob? :/")
    user, _ = await get_user_from_event(event)
    if not user:
        return
    try:
        unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
        if is_muted(user.id, event.chat_id):
            unmute(user.id, event.chat_id)
            await event.reply(f"[{user.first_name}]({unid}) is unmuted in {event.chat.title}")
        else:
            return await event.reply("`This user can already speak freely in this chat`")
    except Exception as e:
        return await event.reply(f"**Error : **`{e}`")
    if EVENT_LOGGER:
        await tbot.send_message(
            EVENT_LOGS,
            "#UNMUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {event.chat.title}(`{event.chat_id}`)"
        )

__mod_name__ = "Delmute"
__help__ = """Delmute

Usage:
> /delmute <reply to anyone> or <user id>
> /undelmute <reply to muted user> or <user id>

Will delete any incoming message from the muted user (even admin)."""