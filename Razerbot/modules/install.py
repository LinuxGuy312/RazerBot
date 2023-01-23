import contextlib
import importlib
import sys
import os
from pathlib import Path
from Razerbot import LOGGER as LOGS, telethn as tbot
from Razerbot.modules.helper_funcs.chat_status import dev_plus 
from Razerbot.events import register

MOD_INFO = {}
LOADED_CMDS = {}
LOAD_PLUG = {}


def load_module(shortname, module_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"Razerbot/modules/{shortname}.py")
        checkmodules(path)
        name = f"Razerbot.modules.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info(f"Successfully installed {shortname}")
    else:
        if module_path is None:
            path = Path(f"Razerbot/modules/{shortname}.py")
            name = f"Razerbot.modules.{shortname}"
        else:
            path = Path((f"{module_path}/{shortname}.py"))
            name = f"{module_path}/{shortname}".replace("/", ".")
        checkmodules(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # for imports
        sys.modules[f"Razerbot.modules.{shortname}"] = mod
        LOGS.info(f"Successfully imported {shortname}")

def remove_module(shortname):
    try:
        cmd = []
        if shortname in MOD_INFO:
            cmd += MOD_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    tbot.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    with contextlib.suppress(BaseException):
        for i in LOAD_PLUG[shortname]:
            tbot.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    try:
        name = f"Razerbot.modules.{shortname}"
        for i in reversed(range(len(catub._event_builders))):
            ev, cb = tbot._event_builders[i]
            if cb.__module__ == name:
                del tbot._event_builders[i]
    except BaseException as exc:
        raise ValueError from exc


def checkmodules(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)

@dev_plus
@register(pattern="^[/!]install$")
async def install(event):
    "To install an external module."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "Razerbot/modules/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.reply(
                    f"Installed Module `{os.path.basename(downloaded_file_name)}`"
                )
            else:
                os.remove(downloaded_file_name)
                await event.reply(
                    "Errors! This module is already installed/pre-installed.", 10
                )
        except Exception as e:
            await event.reply(f"**Error:**\n`{e}`")
            os.remove(downloaded_file_name)

@dev_plus
@register(pattern="^[/!]uninstall ([\s\S]*)")
async def uninstall(event):
    "To uninstall a module."
    shortname = event.pattern_match.group(1)
    path = f"./Razerbot/modules/{shortname}.py"
    if not os.path.exists(path):
        return await event.reply(
            f"There is no module with path {path} to uninstall it"
        )
    os.remove(path)
    try:
        remove_module(shortname)
        await event.reply(f"{shortname} is Uninstalled successfully")
    except Exception as e:
        await event.reply(f"Successfully uninstalled {shortname}\n{e}")
    if shortname in MOD_INFO:
        MOD_INFO.pop(shortname)