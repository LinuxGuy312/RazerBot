import requests
from validators.url import url
from Razerbot import telethn as tbot
from telethon import Button
from Razerbot.events import register

@register(pattern="^[!/.]dns(?:\s|$)([\s\S]*)")
async def _(event):
    #To get Domain Name System(dns) of the given link.
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("ᴇɪᴛʜᴇʀ ʀᴇᴘʟʏ ᴛᴏ ʟɪɴᴋ ᴏʀ ɢɪᴠᴇ ʟɪɴᴋ ᴀs ɪɴᴘᴜᴛ ᴛᴏ ɢᴇᴛ ᴅᴀᴛᴀ")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("ᴛʜᴇ ɢɪᴠᴇɴ ʟɪɴᴋ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
    sample_url = f"https://da.gd/dns/{input_str}"
    if response_api := requests.get(sample_url).text:
        await event.reply(f"ᴅɴs ʀᴇᴄᴏʀᴅs ᴏꜰ {input_str} ᴀʀᴇ \n{response_api}")
    else:
        await event.reply(f"__ɪ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ꜰɪɴᴅ `{input_str}` ᴏɴ ᴛʜᴇ ɪɴᴛᴇʀɴᴇᴛ__")


@register(pattern="^[!/.]short(?:\s|$)([\s\S]*)")
async def _(event):
    #shortens the given link
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("ᴇɪᴛʜᴇʀ ʀᴇᴘʟʏ ᴛᴏ ʟɪɴᴋ ᴏʀ ɢɪᴠᴇ ʟɪɴᴋ ᴀs ɪɴᴘᴜᴛ ᴛᴏ ɢᴇᴛ ᴅᴀᴛᴀ")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("ᴛʜᴇ ɢɪᴠᴇɴ ʟɪɴᴋ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    sample_url = f"https://da.gd/s?url={input_str}"
    if response_api := requests.get(sample_url).text:
        await event.reply(f"sʜᴏʀᴛᴇɴᴇᴅ ᴜʀʟ:\n\n`{response_api}`")
    else:
        await event.reply("sᴏᴍᴇᴛʜɪɴɢ ɪs ᴡʀᴏɴɢ, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")


@register(pattern="^[!/.]unshort(?:\s|$)([\s\S]*)")
async def _(event):
    #To unshort the given dagb shorten url.
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("ᴇɪᴛʜᴇʀ ʀᴇᴘʟʏ ᴛᴏ ʟɪɴᴋ ᴏʀ ɢɪᴠᴇ ʟɪɴᴋ ᴀs ɪɴᴘᴜᴛ ᴛᴏ ɢᴇᴛ ᴅᴀᴛᴀ")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("ᴛʜᴇ ɢɪᴠᴇɴ ʟɪɴᴋ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        button = [Button.url("ʀᴇᴅɪʀᴇᴄᴛᴇᴅ ᴜʀʟ", f"{r.headers['Location']}")]
        await event.reply(f"ʀᴇᴅɪʀᴇᴄᴛᴇᴅ ᴜʀʟ:\n\n`{r.headers['Location']}`", buttons=button)
    else:
        await event.reply(f"ɪɴᴘᴜᴛ ᴜʀʟ {input_str} ʀᴇᴛᴜʀɴᴇᴅ sᴛᴀᴛᴜs_ᴄᴏᴅᴇ {r.status_code}")


@register(pattern="^[!/.]hl(?:\s|$)([\s\S]*)")
async def _(event):
    #To hide the url with white spaces using hyperlink.
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("ᴇɪᴛʜᴇʀ ʀᴇᴘʟʏ ᴛᴏ ʟɪɴᴋ ᴏʀ ɢɪᴠᴇ ʟɪɴᴋ ᴀs ɪɴᴘᴜᴛ ᴛᴏ ɢᴇᴛ ᴅᴀᴛᴀ")
    check = url(input_str)
    if not check:
        catstr = f"http://{input_str}"
        check = url(catstr)
    if not check:
        return await event.reply("ᴛʜᴇ ɢɪᴠᴇɴ ʟɪɴᴋ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")
    await event.delete()
    await event.respond(f"[ㅤㅤㅤㅤㅤㅤㅤ]({input_str})", link_preview=False)
