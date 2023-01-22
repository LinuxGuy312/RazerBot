import html
import re
import os
import requests
import datetime
import platform
import time

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity, __version__ as ptbver, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html
    
from Razerbot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    INFOPIC,
    dispatcher,
    sw,
    StartTime,
    SUPPORT_CHAT,
    BOT_NAME,
)
from Razerbot.__main__ import STATS, TOKEN, USER_INFO
from Razerbot.modules.sql import SESSION
import Razerbot.modules.sql.userinfo_sql as sql
from Razerbot.modules.disable import DisableAbleCommandHandler
from Razerbot.modules.sql.global_bans_sql import is_user_gbanned
from Razerbot.modules.sql.afk_sql import is_afk, set_afk
from Razerbot.modules.sql.users_sql import get_user_num_chats
from Razerbot.modules.helper_funcs.chat_status import sudo_plus
from Razerbot.modules.helper_funcs.extraction import extract_user
from Razerbot import telethn

def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):

        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)

        if is_afk(user.id):
            afkst = set_afk(user.id)
            # if user is afk and no reason then decrease 7%
            # else if reason exist decrease 5%
            new_hp -= no_by_per(total_hp, 7) if not afkst else no_by_per(total_hp, 5)
            # fbanned users will have (2*number of fbans) less from max HP
            # Example: if HP is 100 but user has 5 diff fbans
            # Available HP is (2*5) = 10% less than Max HP
            # So.. 10% of 100HP = 90HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)


def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>Telegram ID:</b>\n"
                f"• {html.escape(user2.first_name)} - <code>{user2.id}</code>.\n"
                f"• {html.escape(user1.first_name)} - <code>{user1.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s ɪᴅ ɪs <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    elif chat.type == "private":
        msg.reply_text(
            f"ʏᴏᴜʀ ɪᴅ ɪs <code>{chat.id}</code>.", parse_mode=ParseMode.HTML,
        )

    else:
        msg.reply_text(
            f"ᴛʜɪs ɢʀᴏᴜᴘ's ɪᴅ ɪs <code>{chat.id}</code>.", parse_mode=ParseMode.HTML,
        )


@telethn.on(
    events.NewMessage(
        pattern="/ginfo ", from_users=(TIGERS or []) + (DRAGONS or []) + (DEMONS or []),
    ),
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins,
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there.",
        )
        return
    msg = f"**ID**: `{entity.id}`"
    msg += f"\n**Title**: `{entity.title}`"
    msg += f"\n**Datacenter**: `{entity.photo.dc_id}`"
    msg += f"\n**Video PFP**: `{entity.photo.has_video}`"
    msg += f"\n**Supergroup**: `{entity.megagroup}`"
    msg += f"\n**Restricted**: `{entity.restricted}`"
    msg += f"\n**Scam**: `{entity.scam}`"
    msg += f"\n**Slowmode**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**Username**: {entity.username}"
    msg += "\n\n**Member Stats:**"
    msg += f"\n`Admins:` `{len(totallist)}`"
    msg += f"\n`Users`: `{totallist.total}`"
    msg += "\n\n**Admins List:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**Description**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)



def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"ɢɪꜰ ɪᴅ:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪꜰ ᴛᴏ ɢᴇᴛ ɪᴛs ɪᴅ.")


def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴇxᴛʀᴀᴄᴛ ᴀ ᴜsᴇʀ ꜰʀᴏᴍ ᴛʜɪs.")
        return

    else:
        return

    rep = message.reply_text("ɢᴇᴛᴛɪɴɢ ɪɴꜰᴏ...")

    text = (
        f"⩘ <b>Usᴇʀ Iɴꜰᴏ</b> ⩗\n"
        f"⋗ ᴜsᴇʀ ɪᴅ: <code>{user.id}</code>\n"
        f"⋗ ꜰɪʀsᴛ ɴᴀᴍᴇ: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n⋗ ʟᴀsᴛ ɴᴀᴍᴇ: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n⋗ ᴜsᴇʀɴᴀᴍᴇ: @{html.escape(user.username)}"

    text += f"\n⋗ ᴜsᴇʀ ᴍᴇɴᴛɪᴏɴ: {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n⋗ ᴩʀᴇsᴇɴᴄᴇ: <code>{}</code>"

        afk_st = is_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"left", "kicked"}:
                    text += _stext.format("ɴᴏᴛ ʜᴇʀᴇ")
                elif status == "member":
                    text += _stext.format("ᴅᴇᴛᴇᴄᴛᴇᴅ")
                elif status in {"administrator", "creator"}:
                    text += _stext.format("ᴀᴅᴍɪɴ")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n\n<b>⋗ ʜᴇᴀʟᴛʜ:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "\n\n<b>ᴛʜɪs ᴘᴇʀsᴏɴ ɪs ʙᴇɪɴɢ sᴘᴀᴍᴡᴀᴛᴄʜᴇᴅ!</b>"
            text += f"\nʀᴇᴀsᴏɴ: <pre>{spamwtc.reason}</pre>"
            text += "\nᴀᴘᴘᴇᴀʟ ᴀᴛ @SpamWatchSupport"
    except:
        pass  # don't crash if api is down somehow...

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏꜰ {BOT_NAME}"
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴀ ᴅᴇᴠ ᴜsᴇʀ ɪɴ {BOT_NAME}"
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴀ ᴅʀᴀɢᴏɴ ɪɴ {BOT_NAME}"
        disaster_level_present = True
    elif user.id in DEMONS:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴀ ᴅᴇᴍᴏɴ ɪɴ {BOT_NAME}"
        disaster_level_present = True
    elif user.id in TIGERS:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴀ ᴛɪɢᴇʀ ɪɴ {BOT_NAME}"
        disaster_level_present = True
    elif user.id in WOLVES:
        text += f"\n\nᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴀ ᴡᴏʟꜰ ɪɴ {BOT_NAME}"
        disaster_level_present = True

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\n<b>⋗ ᴛɪᴛʟᴇ:</b> <code>{custom_title}</code>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            _file = bot.get_file(profile["file_id"])
            _file.download(f"{user.id}.png")

            message.reply_photo(
                photo=open(f"{user.id}.png", "rb"),
                caption=(text),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "「ʜᴇᴀʟᴛʜ」", url="https://t.me/Razer312Updates/4"),
                            InlineKeyboardButton(
                                "「ᴅɪsᴀsᴛᴇʀ」", url="https://t.me/Razer312Updates/6")
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text, 
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "「ʜᴇᴀʟᴛʜ」", url="https://t.me/Razer312Updates/4"),
                            InlineKeyboardButton(
                                "「ᴅɪsᴀsᴛᴇʀ」", url="https://t.me/Razer312Updates/6")
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

    else:
        message.reply_text(
            text, parse_mode=ParseMode.HTML,
        )

    rep.delete()


def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀsɴ'ᴛ sᴇᴛ ᴀɴ ɪɴꜰᴏ ᴍᴇssᴀɢᴇ ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!",
        )
    else:
        update.effective_message.reply_text("ᴛʜᴇʀᴇ ɪsɴᴛ ᴏɴᴇ, ᴜsᴇ /setme ᴛᴏ sᴇᴛ ᴏɴᴇ.")


def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("ᴇʀʀᴏʀ! ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("ᴀᴜᴛʜᴏʀɪᴢᴇᴅ...ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ!")
            elif user_id == bot.id:
                message.reply_text("ɪ ʜᴀᴠᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴍʏ ɪɴꜰᴏ ᴡɪᴛʜ ᴛʜᴇ ᴏɴᴇ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ!")
            else:
                message.reply_text("ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ!")
        else:
            message.reply_text(
                "ᴛʜᴇ ɪɴꜰᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ʜᴀᴠᴇ {}.".format(
                    MAX_MESSAGE_LENGTH // 4,
                    len(info[1]),
                ),
            )

def stats(update: Update, context: CallbackContext):
    stats = f"<b>⌁ ᴄᴜʀʀᴇɴᴛ {BOT_NAME}'s sᴛᴀᴛɪsᴛɪᴄs ⌁</b>\n" + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(
        result,
        parse_mode=ParseMode.HTML, 
        disable_web_page_preview=True
   )
        
        
def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀsɴ'ᴛ ʜᴀᴅ ᴀ ᴍᴇssᴀɢᴇ sᴇᴛ ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!\nsᴇᴛ ᴏɴᴇ ᴜsɪɴɢ /setbio",
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ʜᴀᴅ ᴀ ʙɪᴏ sᴇᴛ ᴀʙᴏᴜᴛ ʏᴏᴜʀsᴇʟꜰ ʏᴇᴛ!",
        )


def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "ʜᴀ, ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴇʀᴄʏ ᴏꜰ ᴏᴛʜᴇʀs ʜᴇʀᴇ...",
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪsᴇᴅ")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "ᴇʀᴍ... ʏᴇᴀʜ, ɪ ᴏɴʟʏ ᴛʀᴜsᴛ ᴛʜᴇ ᴀᴄᴋᴇʀᴍᴀɴs ᴛᴏ sᴇᴛ ᴍʏ ʙɪᴏ.",
            )
            return

        text = message.text
        bio = text.split(
            None, 1,
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "ᴜᴘᴅᴀᴛᴇᴅ {}'s ʙɪᴏ!".format(repl_message.from_user.first_name),
                )
            else:
                message.reply_text(
                    "ʙɪᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ sᴇᴛ {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1]),
                    ),
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ ᴛᴏ sᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>ᴀʙᴏᴜᴛ ᴜsᴇʀ:</b>\n{me}\n"
    if bio:
        result += f"<b>ᴡʜᴀᴛ ᴏᴛʜᴇʀs sᴀʏ:</b>\n{bio}\n"
    result = result.strip("\n")
    return result

__help__ = """
*Away from group*
 ⋗ /afk <reason>*:* mark yourself as AFK(away from keyboard).
 ⋗ brb <reason>*:* same as the afk command - but not a command.
When marked as AFK, any mentions will be replied to with a message to say you're not available!

*ID:*
 ⋗ /id*:* get the current group id. If used by replying to a message, gets that user's id.
 ⋗ /gifid*:* reply to a gif to me to tell you its file ID.

*Self addded information:* 
 ⋗ /setme <text>*:* will set your info
 ⋗ /me*:* will get your or another user's info.
*Examples:* 💡
 ➩ /setme I am a wolf.
 ➩ /me @username(defaults to yours if no user specified)

*Information others add on you:* 
 ⋗ /bio*:* will get your or another user's bio. This cannot be set by yourself.
 ⋗ /setbio <text>*:* while replying, will save another user's bio 
*Examples:* 💡
 ➩ /bio @username(defaults to yours if not specified).`
 ➩ /setbio This user is a wolf` (reply to the user)

*Overall Information about you:*
 ⋗ /info*:* get information about a user. 

 *Info about group:*
 ⋗ /ginfo <group-id/username>*:* get information about group.
 
*What is that health thingy?*
 Come and see [HP System explained](https://t.me/Razer312Updates/4)
"""

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio)

STATS_HANDLER = CommandHandler("stats", stats)
ID_HANDLER = DisableAbleCommandHandler("id", get_id)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid)
INFO_HANDLER = DisableAbleCommandHandler(("info", "book"), info)
GRP_INFO_HANDLER = DisableAbleCommandHandler("ginfo", group_info)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "Iɴғᴏs"
__command_list__ = ["setbio", "bio", "setme", "me", "info", "ginfo"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
