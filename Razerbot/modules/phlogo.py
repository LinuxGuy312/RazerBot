import os
from Razerbot import telethn as tbot
from Razerbot.events import register
try:
	from phlogo import generate
except ModuleNotFoundError:
	os.system("pip install phlogo")
	from phlogo import generate

@register(pattern="^/phlogo ?(.*)")
async def ph(event):
    query = event.pattern_match.group(1)
    p = query.split(" ", 1)[0]
    h = query.split(" ", 1)[1]
    reply_to_id = event.reply_to_msg_id
    result = generate(f"{p}",f"{h}")
    result.save("ph.png")
    pic = "/root/Razerbot/ph.png"
    await event.client.send_file(event.chat_id, pic, reply_to=event.reply_to_msg_id, forcedocument=False)
    os.remove(pic)