import html
import re
from time import sleep

import requests
from googletrans import Translator
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import Razerbot.modules.sql.chatbot_sql as sql
from Razerbot import dispatcher, BOT_NAME
from Razerbot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from Razerbot.modules.helper_funcs.filters import CustomFilters
from Razerbot.modules.log_channel import gloggable

tr = Translator()


@user_admin_no_reply
@gloggable
def razerrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_razer = sql.rem_razer(chat.id)
        if is_razer:
            is_razer = sql.rem_razer(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"Razer Chatbot Disable\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Razer Chatbot disable by {}.".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def razeradd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_razer = sql.set_razer(chat.id)
        if is_razer:
            is_razer = sql.set_razer(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"Razer Chatbot Enable\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Razer Chatbot enable by {}.".format(
                    mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def razer(update: Update, context: CallbackContext):
    update.effective_user
    message = update.effective_message
    msg = """**Welcome To Control Panal Of Razer ChatBot**

**Here You Will Find Two Buttons Select AnyOne Of Them**"""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="On", callback_data="add_chat({})"),
                InlineKeyboardButton(text="Off", callback_data="rm_chat({})"),
            ]
        ]
    )
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )


def razer_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "razer":
        return True
    if reply_message:
        if reply_message.from_user.id == context.bot.get_me().id:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_razer = sql.is_razer(chat_id)
    if not is_razer:
        return

    if message.text and not message.document:
        if not razer_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        url = f"https://kora-api.vercel.app/chatbot/2d94e37d-937f-4d28-9196-bd5552cac68b/{BOT_NAME}/Razer/message={message.text}"
        request = requests.get(url)
        results = json.loads(request.text)
        sleep(0.5)
        message.reply_text(results["reply"])


def list_all_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_razer_chats()
    text = "<b>Razer-Enabled Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"• <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            sql.rem_razer(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")


__mod_name__ = "Chatbot 🤖"
__help__ = """
Razer AI ChatBot is the only ai system which can detect & reply upto 200 language's

❂ `/token` : To get your Razer Chatbot Token.
❂ `/chatbot`: To On Or Off ChatBot In Your Chat.

*Reports bugs at*: @Razer312Support
*Powered by* @Razer312bot"""

CHATBOTK_HANDLER = CommandHandler("chatbot", razer)
ADD_CHAT_HANDLER = CallbackQueryHandler(razeradd, pattern=r"add_chat")
RM_CHAT_HANDLER = CallbackQueryHandler(razerrm, pattern=r"rm_chat")
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
)
LIST_ALL_CHATS_HANDLER = CommandHandler(
    "allchats", list_all_chats, filters=CustomFilters.dev_filter
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
    CHATBOT_HANDLER,
]
