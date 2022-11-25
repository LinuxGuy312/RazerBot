import io
import traceback
from datetime import datetime

import requests
from selenium import webdriver
from validators.url import url

from Razerbot import telethn as tbot
from Razerbot import register


@register(pattern="/(webss|gis) ([\s\S]*)")
async def _(event):
    "To Take a screenshot of a website."
    CHROME_BIN = "/usr/bin/google-chrome"
    razevent = await event.reply('`Processing..`')
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = CHROME_BIN
        driver = webdriver.Chrome(chrome_options=chrome_options)
        cmd = event.pattern_match.group(1)
        input_str = event.pattern_match.group(2)
        inputstr = input_str
        if cmd == "ss":
            razurl = url(inputstr)
            if not razurl:
                inputstr = f"http://{input_str}"
                razurl = url(inputstr)
            if not razurl:
                return await razevent.edit("`The given input is not supported url`")
        if cmd == "gis":
            inputstr = f"https://www.google.com/search?q={input_str}"
        driver.get(inputstr)
        await catevent.edit("`Calculating Page Dimensions`")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        im_png = driver.get_screenshot_as_png()
        driver.close()
        end = datetime.now()
        ms = (end - start).seconds
        hmm = f"**URL : **{input_str} \n**Time :** `{ms} seconds`"
        await catevent.delete()
        with io.BytesIO(im_png) as out_file:
            out_file.name = f"{input_str}.PNG"
            await tbot.send_file(
                event.chat_id,
                out_file,
                caption=hmm,
                force_document=True,
                reply_to=event.message.id,
                allow_cache=False,
                silent=True,
            )
    except Exception:
        await razevent.edit(f"`{traceback.format_exc()}`")
