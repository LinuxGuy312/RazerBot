import os

from Razerbot import telethn as tbot
from Razerbot.events import register
from telethon import Button, types

TMP_DOWNLOAD_DIRECTORY = "./"

from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions


razer = "Razerbot"
telegraph = Telegraph()
data = telegraph.create_account(short_name=razer)
auth_url = data["auth_url"]


@register(pattern="^[!/.]tg(m|t) ?(.*)")
async def tgph(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "m":
            downloaded_file_name = await tbot.download_media(
                r_message, TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply(
                "Downloaded to {} in {} seconds.".format(downloaded_file_name, ms)
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                (end - start).seconds
                os.remove(downloaded_file_name)
                await h.delete()
                buttons = [
                    Button.url("View Telegraph", f"https://te.legra.ph{media_urls[0]}")
                ]
                await tbot.send_message(
                    event.chat_id,
                    "Uploaded to https://te.legra.ph{})".format(media_urls[0]),
                    link_preview=True,
                    buttons=buttons,
                    reply_to=event.reply_to_msg_id
                )
        elif input_str == "t":
            user_object = await tbot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tbot.download_media(
                    r_message, TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            await event.delete()
            buttons = [
                Button.url("View Telegraph", f"https://telegra.ph/{response['path']}")
            ]
            await tbot.send_message(
                event.chat_id,
                "Pasted to https://telegra.ph/{} in {} seconds.".format(
                    response["path"], ms
                ),
                link_preview=True,
                buttons=buttons,
                reply_to=event.reply_to_msg_id
            )
    else:
        await event.reply("Reply to a message to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")