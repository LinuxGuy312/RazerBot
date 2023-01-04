from typing import Dict, Union

from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

from Razerbot import MONGO_DB_URI

mongo = MongoCli(MONGO_DB_URI)
db = mongo.Razerbot

afkdb = db.afk
coupledb = db.couple
karmadb = db.karma


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]

async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )

async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})

async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list


async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers

async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False

async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers}},
        upsert=True,
    )


async def get_karmas_count() -> dict:
    chats_count = 0
    karmas_count = 0
    async for chat in karmadb.find({"chat_id": {"$lt": 0}}):
        for i in chat["karma"]:
            karma_ = chat["karma"][i]["karma"]
            if karma_ > 0:
                karmas_count += karma_
        chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}

async def user_global_karma(user_id) -> int:
    total_karma = 0
    async for chat in karmadb.find({"chat_id": {"$lt": 0}}):
        karma = await get_karma(chat["chat_id"], await int_to_alpha(user_id))
        if karma and (int(karma["karma"]) > 0):
            total_karma += int(karma["karma"])
    return total_karma

async def get_karmas(chat_id: int) -> Dict[str, int]:
    karma = await karmadb.find_one({"chat_id": chat_id})
    if not karma:
        return {}
    return karma["karma"]

async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    if name in karmas:
        return karmas[name]

async def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    karmas[name] = karma
    await karmadb.update_one(
        {"chat_id": chat_id}, {"$set": {"karma": karmas}}, upsert=True
    )

async def is_karma_on(chat_id: int) -> bool:
    chat = await karmadb.find_one({"chat_id_toggle": chat_id})
    if not chat:
        return True
    return False


async def karma_on(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if is_karma:
        return
    return await karmadb.delete_one({"chat_id_toggle": chat_id})

async def karma_off(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if not is_karma:
        return
    return await karmadb.insert_one({"chat_id_toggle": chat_id})


async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text

async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id
