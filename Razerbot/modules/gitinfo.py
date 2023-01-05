from aiohttp import ClientSession
from pyrogram import filters

from Razerbot import pbot
from Razerbot.utils.errors import capture_err


@pbot.on_message(filters.command(["github", "git"]))
@capture_err
async def github(_, message):
    h = await message.reply_text("Gathering Info...")
    if len(message.command) != 2:
        return await message.reply_text("Usage : /git username")
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")
            result = await request.json()
            try:
                url = result["html_url"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]
                caption = f"""**Iɴғᴏ Oғ {username}**
**Usᴇʀɴᴀᴍᴇ :** `{username}`
**Bɪᴏ :** `{bio}`
**Pʀᴏғɪʟᴇ Lɪɴᴋ :** [Here]({url})
**Cᴏᴍᴘᴀɴʏ :** `{company}`
**Cʀᴇᴀᴛᴇᴅ Oɴ :** `{created_at}`
**Rᴇᴘᴏsɪᴛᴏʀɪᴇs :** `{repositories}`
**Bʟᴏɢ :** `{blog}`
**Lᴏᴄᴀᴛɪᴏɴ :** `{location}`
**Fᴏʟʟᴏᴡᴇʀs :** `{followers}`
**Fᴏʟʟᴏᴡɪɴɢ :** `{following}`"""
            except:
                print(str(e))
    await h.delete()
    await message.reply_photo(photo=avatar_url, caption=caption)


__mod_name__ = "Gɪᴛʜᴜʙ"

__help__ = """
I will give information about github profile 

 ❍ /github <username>*:* Get information about a GitHub user.
"""