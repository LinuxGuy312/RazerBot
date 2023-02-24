import re
import io
import os
import sys
import traceback
import asyncio 
from time import time
from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Razerbot import DRAGONS, pbot as app, DEV_USERS


def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset

def yaml_format(obj, indent=0, max_str_len=256, max_byte_len=64):
    result = []

    if isinstance(obj, dict):
        if not obj:
            return "dict:"
        items = obj.items()
        has_items = len(items) > 1
        has_multiple_items = len(items) > 2
        result.append(obj.get("_", "dict") + (":" if has_items else ""))
        if has_multiple_items:
            result.append("\n")
            indent += 2
        for k, v in items:
            if k == "_" or v is None:
                continue
            formatted = yaml_format(v, indent)
            if not formatted.strip():
                continue
            result.append(" " * (indent if has_multiple_items else 1))
            result.append(f"{k}:")
            if not formatted[0].isspace():
                result.append(" ")
            result.append(f"{formatted}")
            result.append("\n")
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2
    elif isinstance(obj, str):
        result = repr(obj[:max_str_len])
        if len(obj) > max_str_len:
            result += "…"
        return result
    elif isinstance(obj, bytes):
        if all(0x20 <= c < 0x7F for c in obj):
            return repr(obj)
        return "<…>" if len(obj) > max_byte_len else " ".join(f"{b:02X}" for b in obj)
    elif isinstance(obj, datetime):
        return utc_to_local(obj).strftime("%Y-%m-%d %H:%M:%S")
    elif hasattr(obj, "__iter__"):
        result.append("\n")
        indent += 2
        for x in obj:
            result.append(f"{' ' * indent}- {yaml_format(x, indent + 2)}")
            result.append("\n")
        result.pop()
        indent -= 2
    else:
        return repr(obj)
    return "".join(result)
  


async def aexec_(code, smessatatus, client):
    message = event = m = smessatatus
    p = lambda _x: print(yaml_format(_x))
    exec("async def __aexec(message, event, client, p): "
            + "".join(f"\n {l}" for l in code.split("\n")))
  
    return await locals()["__aexec"](
        message, event, client, p
    )
  

@app.on_edited_message(filters.command("eval", prefixes=["/", "!"]) & filters.user(DRAGONS) & ~filters.forwarded)
@app.on_message(filters.command("eval", prefixes=["/", "!"]) & filters.user(DRAGONS) & ~filters.forwarded)
async def eval(client, message):
    if message.from_user.id not in DEV_USERS:
        return await message.reply_text("ᴛʜɪs ɪs ᴀ ᴅᴇᴠᴇʟᴏᴘᴇʀ ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅ.\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ʀᴜɴ ᴛʜɪs.")
    cmd = "".join(message.text.split(maxsplit=1)[1:])
    if "config.py" in cmd:
        return await message.reply_text(f"#PRIVACY_ERROR\nCan't access config.py`")
    print(cmd)
    if not cmd:
        return await message.reply_text("ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ ʀᴜɴ?")
    eva = await message.reply_text("ʀᴜɴɴɪɴɢ...")
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec_(cmd, message, client)
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
    final_output = (f"⥤ ᴇᴠᴀʟ : \n```{cmd}``` \n\n⥤ ʀᴇsᴜʟᴛ : \n```{evaluation}```")
    if len(final_output) > 4096:
        filename = "result.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"**INPUT:**\n`{cmd[0:980]}`\n\n**OUTPUT:**\n`Attached Document`",
            quote=False,
            reply_markup=keyboard,
        )
        await eva.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await eva.delete()
        await message.reply(text=final_output, reply_markup=keyboard)
    
@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)