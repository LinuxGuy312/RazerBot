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
	if query == "":
		await event.reply("Give some text bruh, e.g.: `/phlogo Razer Bot`")
		return
	try:
		p = query.split(" ", 1)[0]
		h = query.split(" ", 1)[1]
	except:
		await event.reply("Something went wrong, try giving two words. e.g.: `/phlogo Razer Bot`")
		return
	result = generate(f"{p}",f"{h}")
	pic = "ph.png"
	result.save(pic, "png")
	await tbot.send_file(event.chat_id, pic, reply_to=event.message.id, forcedocument=False)
	os.remove(pic)
