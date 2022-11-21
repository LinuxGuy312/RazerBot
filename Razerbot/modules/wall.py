import os
import random

import requests
from bs4 import BeautifulSoup

from Razerbot import telethn, SUPPORT_GROUP
from Razerbot.events import register

async def wall_download(piclink, query):
    try:
        if not os.path.isdir("./temp"):
            os.mkdir("./temp")
        picpath = f"./temp/{query.title().replace(' ', '')}.jpg"
        if os.path.exists(picpath):
            i = 1
            while os.path.exists(picpath) and i < 11:
                picpath = f"./temp/{query.title().replace(' ', '')}-{i}.jpg"
                i += 1
        with open(picpath, "wb") as f:
            f.write(requests.get(piclink).content)
        return picpath
    except Exception as e:
        event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ @{SUPPORT_GROUP}, {e}')
        return None

@register(pattern="^/wall ?(.*)")
async def wall(event):
    query = event.pattern_match.group(1)
    limit = 1
    if not query:
        return await event.reply("ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ sᴇᴀʀᴄʜ?")
    if ";" in query:
        query, limit = query.split(";")
    if int(limit) > 10:
        return await event.reply("ᴡᴀʟʟᴘᴀᴘᴇʀ sᴇᴀʀᴄʜ ʟɪᴍɪᴛ ɪs 1-10")
    sear = await event.reply('🔍 sᴇᴀʀᴄʜɪɴɢ...')
    r = requests.get(
        f"https://wall.alphacoders.com/search.php?search={query.replace(' ','+')}"
    )
    soup = BeautifulSoup(r.content, "lxml")
    walls = soup.find_all("img", class_="img-responsive")
    if not walls:
        return await sear.edit(f"ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴀɴʏᴛʜɪɴɢ ᴡɪᴛʜ : `{query}`")
    i = count = 0
    capcount = 1
    piclist = []
    piclinks = []
    captionlist = []
    await sear.edit("⏳ ᴘʀᴏᴄᴇssɪɴɢ...")
    url2 = "https://api.alphacoders.com/content/get-download-link"
    for x in walls:
        wall = random.choice(walls)["src"][8:-4]
        server = wall.split(".")[0]
        fileid = wall.split("-")[-1]
        data = {
            "content_id": fileid,
            "content_type": "wallpaper",
            "file_type": "jpg",
            "image_server": server,
        }
        res = requests.post(url2, data=data)
        try:
            a = res.json()["link"]
        except KeyError:
            return await sear.edit("ʜᴍᴍ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏᴛʜɪɴɢ. sᴏʀʀʏ.")
        if "We are sorry," not in requests.get(a).text and a not in piclinks:
            await sear.edit("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
            pic = await wall_download(a, query)
            if pic is None:
                return await edit_delete("sᴏʀʀʏ, ᴄᴀɴ'ᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴡᴀʟʟᴘᴀᴘᴇʀ.")
            piclist.append(pic)
            piclinks.append(a)
            captionlist.append("")
            count += 1
            i = 0
        else:
            i += 1
        await sear.edit(f"📥 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ : {count}/{limit}\n\n❌ ᴇʀʀᴏʀs : {i}/{limit}")
        if count == int(limit):
            break
        if i == 5:
            await sear.edit("ᴍᴀx sᴇᴀʀᴄʜ ᴇʀʀᴏʀ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅ.")
    try:
        await sear.edit("sᴇɴᴅɪɴɢ...")
        captionlist[-1] = f"⇛ ǫᴜᴇʀʏ :- {query.title()}"
        await telethn.send_file(
            event.chat_id,
            piclist,
            caption=captionlist,
            reply_to=event.reply_to_msg_id,
            force_document=True,
        )
        await sear.delete()
    except Exception as e:
        await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ @{SUPPORT_GROUP}, {e}')
    for i in piclist:
        os.remove(i)
