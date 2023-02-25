# For CatUB By MineisZarox https://t.me/IrisZarox (Demon), Ported to pyrogram By https://telegram.dog/WH0907 (Eren)
import asyncio
import io
import os
import time
from pathlib import Path
from typing import Dict, Tuple

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

from Razerbot import pbot, OWNER_ID


CC = []
PATH = []  # using list method for some reason

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"

# freaking selector
def add_s(msg, num: int):
    fmsg = ""
    msgs = msg.splitlines()
    leng = len(msgs)
    if num == 0:
        valv = leng - 1
        msgs[valv] = msgs[valv] + " ❇️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    elif num == leng:
        valv = 1
        msgs[valv] = msgs[valv] + " ❇️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    else:
        valv = num
        msgs[valv] = msgs[valv] + " ❇️"
        for ff in msgs:
            fmsg += f"{ff}\n"
    buttons = [
        [
            IKB("D", callback_data=f"fmrem_{msgs[valv]}|{valv}"),
            IKB("X", callback_data=f"fmcut_{msgs[valv]}|{valv}"),
            IKB("C", callback_data=f"fmcopy_{msgs[valv]}|{valv}"),
            IKB("V", callback_data=f"fmpaste_{valv}"),
        ],
        [
            IKB("⇚", callback_data="fmback"),
            IKB("⤊", callback_data=f"fmup_{valv}"),
            IKB("⤋", callback_data=f"fmdown_{valv}"),
            IKB("⇛", callback_data=f"fmforth_{msgs[valv]}"),
        ],
    ]
    return fmsg, buttons

def get_manager(path, num: int):
    if os.path.isdir(path):
        msg = "Folders and Files in `{}` :\n".format(path)
        lists = sorted(os.listdir(path))
        files = ""
        folders = ""
        for contents in sorted(lists):
            zpath = os.path.join(path, contents)
            if not os.path.isdir(zpath):
                size = os.stat(zpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎧`{contents}`\n"
                if str(contents).endswith((".opus")):
                    files += f"🎤`{contents}`\n"
                elif str(contents).endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += f"🎬`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"📚`{contents}`\n"
                elif str(contents).endswith((".py")):
                    files += f"🐍`{contents}`\n"
                elif str(contents).endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")
                ):
                    files += f"🏞`{contents}`\n"
                else:
                    files += f"📔`{contents}`\n"
            else:
                folders += f"📂`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
        PATH.clear()
        PATH.append(path)
        msgs = add_s(msg, int(num))
    else:
        size = os.stat(path).st_size
        msg = "The details of given file :\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎧"
        if str(path).endswith((".opus")):
            mode = "🎤"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎬"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "📚"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🏞"
        elif str(path).endswith((".py")):
            mode = "🐍"
        else:
            mode = "📔"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{path}`\n"
        msg += f"**icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"
        buttons = [
            [
                IKB("D", callback_data=f"fmrem_File|{num}"),
                IKB("S", callback_data="fmsend"),
                IKB("X", callback_data=f"fmcut_File|{num}"),
                IKB("C", callback_data=f"fmcopy_File{num}"),
            ],
            [
                IKB("⇚", callback_data="fmback"),
                IKB("⤊", callback_data="fmup_File"),
                IKB("⤋", callback_data="fmdown_File"),
                IKB("⇛", callback_data="fmforth_File"),
            ],
        ]
        PATH.clear()
        PATH.append(path)
        msgs = (msg, buttons)
    return msgs


# BACK
@pbot.on_callback_query(filters.regex("fmback"))
async def back(_, m):
    path = PATH[0]
    paths = path.split("/")
    if paths[-1] == "":
        paths.pop()
        paths.pop()
    else:
        paths.pop()
    npath = ""
    for ii in paths:
        npath += f"{ii}/"
    num = 1
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await m.message.edit_text(msg, reply_markup=IKM(buttons))


# UP
@pbot.on_callback_query(filters.regex("fmup_(.*)"))
async def up(_, m):
    num = m.matches[0].group(1)
    if num == "File":
        await m.answer("Its a File dummy!", show_alert=True)
    else:
        num1 = int(num) - 1
        path = PATH[0]
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))


# DOWN
@pbot.on_callback_query(filters.regex("fmdown_(.*)"))
async def down(bot, m):
    num = m.matches[0].group(1)
    if num == "File":
        await m.answer("Its a file dummy!", show_alert=True)
    else:
        path = PATH[0]
        num1 = int(num) + 1
        msg, buttons = get_manager(path, num1)
        await asyncio.sleep(1)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))


# FORTH
@pbot.on_callback_query(filters.regex("fmforth_(.*)"))
async def forth(_, m):
    npath = m.matches[0].group(1)
    if npath == "File":
        await m.answer("Its a file dummy!", show_alert=True)
    else:
        path = PATH[0]
        npath = npath[2:-4]
        rpath = f"{path}/{npath}"
        num = 1
        msg, buttons = get_manager(rpath, num)
        await asyncio.sleep(1)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))


# REMOVE
@pbot.on_callback_query(filters.regex("fmrem_(.*)"))
async def remove(_, m):
    fn, num = (m.matches[0].group(1)).split("|", 1)
    path = PATH[0]
    if fn == "File":
        paths = path.split("/")
        if paths[-1] == "":
            paths.pop()
            paths.pop()
        else:
            paths.pop()
        npath = ""
        for ii in paths:
            npath += f"{ii}/"
        rpath = path
    else:
        n_path = fn[2:-4]
        rpath = f"{path}/{n_path}"
        npath = path
    msg, buttons = get_manager(npath, num)
    await asyncio.sleep(1)
    await m.message.edit_text(msg, reply_markup=IKM(buttons))
    await runcmd(f"rm -rf '{rpath}'")
    await m.answer(f"{rpath} removed successfully...")


# SEND
@pbot.on_callback_query(filters.regex("fmsend"))
async def send(_, m):
    path = PATH[0]
    uploaded = await m.message.reply_document(file=path, caption='Uploaded By Razer.')


# CUT
@pbot.on_callback_query(filters.regex("fmcut_(.*)"))
async def cut(_, m):
    f, n = (m.matches[0].group(1)).split("|", 1)
    if CC:
        return await m.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("cut")
            CC.append(npath)
            await m.answer(f"Moving {npath} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("cut")
            CC.append(rpath)
            await m.answer(f"Moving {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))


# COPY
@pbot.on_callback_query(filters.regex("fmcopy_(.*)"))
async def copy(_, m):
    f, n = (m.matches[0].group(1)).split("|", 1)
    if CC:
        return await m.answer(f"Paste {CC[1]} first")
    else:
        if f == "File":
            npath = PATH[0]
            paths = npath.split("/")
            if paths[-1] == "":
                paths.pop()
                paths.pop()
            else:
                paths.pop()
            path = ""
            for ii in paths:
                path += f"{ii}/"
            CC.append("copy")
            CC.append(npath)
            await m.answer(f"Copying {path} ...")
        else:
            path = PATH[0]
            npath = f[2:-4]
            rpath = f"{path}/{npath}"
            CC.append("copy")
            CC.append(rpath)
            await m.answer(f"Copying {rpath} ...")
        msg, buttons = get_manager(path, n)
        await asyncio.sleep(1)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))


# PASTE
@pbot.on_callback_query(filters.regex("fmpaste_(.*)"))
async def paste(_, m):
    n = m.matches[0].group(1)
    path = PATH[0]
    if CC:
        if CC[0] == "cut":
            cmd = f"mv '{CC[1]}' '{path}'"
        else:
            cmd = f"cp '{CC[1]}' '{path}'"
        await runcmd(cmd)
        msg, buttons = get_manager(path, n)
        await m.message.edit_text(msg, reply_markup=IKM(buttons))
        CC.clear()
    else:
        await m.answer("You aint copied anything to paste")


@pbot.on_message(filters.command('ls'))
@pbot.on_edited_message(filters.command('ls'))
async def fm(_, m):
    msg, buttons = get_manager(os.getcwd(), 1)
    await m.reply_text(msg, reply_markup=IKM(buttons))