import asyncio
import io
import os
import sys
import traceback

from Razerbot.utils import format as _format
from Razerbot import telethn as tbot
from Razerbot.events import register
from Razerbot import *


@register(pattern="^/razexec(?:\s|$)([\s\S]*)")
async def _(event):
    if event.sender.id not in DEV_USERS:
        return await event.reply("ᴛʜɪs ɪs ᴀ ᴅᴇᴠᴇʟᴏᴘᴇʀ ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅ.\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ʀᴜɴ ᴛʜɪs.")
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.reply("ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ ᴇxᴇᴄᴜᴛᴇ?")
    razevent = await event.reply("ᴇxᴇᴄᴜᴛɪɴɢ...")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    razbot = await tbot.get_me()
    curruser = f"{BOT_USERNAME}"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"```{curruser}:~#``` ```{cmd}```\n```{result}```"
    else:
        cresult = f"```{curruser}:~$``` ```{cmd}```\n```{result}```"
    await razevent.edit(text=cresult,)
    if EVENT_LOGS:
        await event.client.send_message(int(EVENT_LOGS), f"#RAZEXEC\nᴛᴇʀᴍɪɴᴀʟ ᴄᴏᴍᴍᴀɴᴅ `{cmd}` ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sᴜᴄᴇssꜰᴜʟʟʏ ɪɴ `{event.chat_id}`")


@register(pattern="^/razeval(?:\s|$)([\s\S]*)")
async def _(event):
    if event.sender.id not in DEV_USERS:
        return await event.reply("ᴛʜɪs ɪs ᴀ ᴅᴇᴠᴇʟᴏᴘᴇʀ ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅ.\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ʀᴜɴ ᴛʜɪs.")
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.reply("ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ ʀᴜɴ?")
    cmd = (
        cmd.replace("send_message", "send_message")
        .replace("send_file", "send_file")
        .replace("edit_message", "edit_message")
    )
    razevent = await event.reply("ʀᴜɴɴɪɴɢ...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "sᴜᴄᴄᴇss"
    final_output = (
        f"⥤ ᴇᴠᴀʟ : \n```{cmd}``` \n\n⥤ ʀᴇsᴜʟᴛ : \n```{evaluation}``` \n"
    )
    await razevent.edit(text=final_output)
    if EVENT_LOGS:
        await event.client.send_message(int(EVENT_LOGS), f"#RAZEVAL\nᴇᴠᴀʟ ᴄᴏᴍᴍᴀɴᴅ `{cmd}` ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sᴜᴄᴇssꜰᴜʟʟʏ ɪɴ `{event.chat_id}`")


async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(_format.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        (
            "async def __aexec(message, event , reply, client, p, chat): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )

    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
