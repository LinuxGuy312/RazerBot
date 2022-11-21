import requests
from validators.url import url
from Razerbot import telethn as tbot
from Razerbot.events import register


@register(pattern="^/dns(?:\s|$)([\s\S]*)")
async def _(event):
    "To get Domain Name System(dns) of the given link."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("`Either reply to link or give link as input to get data`")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("`the given link is not supported`")
    sample_url = f"https://da.gd/dns/{input_str}"
    if response_api := requests.get(sample_url).text:
        await event.reply(f"DNS records of {input_str} are \n{response_api}")
    else:
        await event.reply(f"__I can't seem to find `{input_str}` on the internet__")


@register(pattern="^/short(?:\s|$)([\s\S]*)")
async def _(event):
    "shortens the given link"
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("Either reply to link or give link as input to get data")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("The given link is not supported")
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    sample_url = f"https://da.gd/s?url={input_str}"
    if response_api := requests.get(sample_url).text:
        await event.reply(f"Shortened URL : {response_api}")
    else:
        await event.reply("Something is wrong, please try again later.")


@register(pattern="^/unshort(?:\s|$)([\s\S]*)")
async def _(event):
    "To unshort the given dagb shorten url."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("Either reply to link or give link as input to get data")
    check = url(input_str)
    if not check:
        razstr = f"http://{input_str}"
        check = url(razstr)
    if not check:
        return await event.reply("The given link is not supported")
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await event.reply(f"ReDirected URL: {r.headers['Location']}")
    else:
        await event.reply(f"Input URL `{input_str}` returned status_code {r.status_code}")


@register(pattern="^/hl(?:\s|$)([\s\S]*)")
async def _(event):
    "To hide the url with white spaces using hyperlink."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await event.reply("Either reply to link or give link as input to get data")
    check = url(input_str)
    if not check:
        catstr = f"http://{input_str}"
        check = url(catstr)
    if not check:
        return await event.reply("`The given link is not supported`")
    await event.reply(f"Hidden Link : [ㅤㅤㅤㅤㅤㅤㅤ]({input_str})")
