import subprocess
from pyrogram import filters
from Razerbot import pbot

@pbot.on_message(filters.regex('^[/!](sysd|neofetch)'))
@pbot.on_edited_message(filters.regex('^[/!](sysd|neofetch)'))
async def neofetch(bot, m):
    cmd = 'neofetch --off --color_blocks off --bold off --cpu_temp C --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout'
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, _ = process.communicate()
    out = stdout.decode()
    await m.reply_text(out)