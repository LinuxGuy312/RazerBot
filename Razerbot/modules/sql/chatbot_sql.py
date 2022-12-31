import threading

from sqlalchemy import Column, String

from Razerbot.modules.sql import BASE, SESSION


class RazerChats(BASE):
    __tablename__ = "razer_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


RazerChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_razer(chat_id):
    try:
        chat = SESSION.query(RazerChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_razer(chat_id):
    with INSERTION_LOCK:
        razerchat = SESSION.query(RazerChats).get(str(chat_id))
        if not razerchat:
            razerchat = RazerChats(str(chat_id))
        SESSION.add(razerchat)
        SESSION.commit()


def rem_razer(chat_id):
    with INSERTION_LOCK:
        razerchat = SESSION.query(RazerChats).get(str(chat_id))
        if razerchat:
            SESSION.delete(razerchat)
        SESSION.commit()


def get_all_razer_chats():
    try:
        return SESSION.query(RazerChats.chat_id).all()
    finally:
        SESSION.close()
