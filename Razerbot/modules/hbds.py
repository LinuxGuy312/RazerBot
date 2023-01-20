import os
import urllib
try:
	from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ModuleNotFoundError:
	os.system("pip install moviepy")
	from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from Razerbot import telethn as tbot
from Razerbot.events import register
from telethon.tl.types import DocumentAttributeAudio

@register(pattern="^[/!]hbds(?: |$)([\s\S]*)")
async def song(hbd):
	dun = await hbd.reply('`Processing...`')
	oof = hbd.pattern_match.group(1)
	jadu = await hbd.get_reply_message()
	if not oof and jadu:
		oof = jadu.text
	if oof == "":
		await hbd.edit("`Give a name!`")
	fh = oof.split()[0]
	fl = fh.title()
	dur = 64
	fn = f"{fl}.mp3"
	me = await hbd.client.get_me()
	firn = me.first_name.replace("\xad", "")
	lasn = me.last_name or ""
	artist = f"{firn} {lasn}"
	img = "https://graph.org/file/89b7edac2ce6befd85257.jpg"
	urllib.request.urlretrieve(img, fl)
	song = f"https://s3-us-west-2.amazonaws.com/1hbcf/{fn}"
	try:
		urllib.request.urlretrieve(song, fn)
	except urllib.error.HTTPError:
		os.remove(fl)
		return await hbd.edit(f"`Sorry couldn't get song for {fl}`")
	await dun.edit('`Almost there...`')
	sfn = f"Happy Birthday {fl}!.mp3"
	sfnl = len(sfn)
	ffmpeg_extract_subclip(fn, 0, dur, targetname=sfn)
	await hbd.client.send_file(hbd.chat_id, sfn, thumb=fl, attributes=[DocumentAttributeAudio(title=sfn[:sfnl-4], performer=artist, duration=dur)], reply_to=hbd.reply_to_msg_id)
	await dun.delete()
	os.remove(fn)
	os.remove(sfn)
	os.remove(fl)

__mod_name__ = "HBD Sᴏɴɢ"
__help__ = """Hᴀᴘᴘʏ Bɪʀᴛʜᴅᴀʏ Sᴏɴɢ

Usage:
> /hbds <name>
> /hbds <reply to name>

Wɪʟʟ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ ʜᴀᴘᴘʏ ʙɪʀᴛʜᴅᴀʏ sᴏɴɢ."""