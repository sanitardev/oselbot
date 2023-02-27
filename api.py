from fastapi import FastAPI
from utils import *
from key_generator.key_generator import generate
import random

app = FastAPI()


@app.get("/randkey")
async def randkey():
    ut = Utils()
    rv = random.choices(
        ["1_viagra", "1_beer", "1_vodka", "2_condoms", "1_condoms", "4_coins", "3_coins", "2_coins", "1_coins"],
        weights=[20, 30, 30, 35, 45, 50, 60, 70, 80], k=1)[0]
    key = generate(10, '-', 5, 5, type_of_value='hex').get_key()
    maxuses = 1
    reward = rv
    ut.insert("keys", "key", key)
    ut.update("keys", "maxuses", maxuses, "key", key)
    ut.update("keys", "reward", reward, "key", key)
    ut.close()
    return f"{key}"


@app.get("/genkey")
async def genkey(item: str, count: int, uses: int):
    ut = Utils()
    if not (item in [i[1].id for i in ut.all_items.items()]):
        ut.close()
        return "error: item not in list"
    elif count < 10000 and count > -10000:
        ut.close()
        return "error: count too big or too small"
    elif uses < 10000 and uses > -10000:
        ut.close()
        return "error: uses too big or too small"
    reward = f"{count}_{item}"
    key = generate(10, '-', 5, 5, type_of_value='hex').get_key()
    ut.insert("keys", "key", key)
    ut.update("keys", "maxuses", uses, "key", key)
    ut.update("keys", "reward", reward, "key", key)
    ut.close()
    return f"{key}"


@app.get("/user/{id}/append")
async def append_user(id: int, item: str, count: int):
    ut = Utils()
    if not (item in [i[1].id for i in ut.all_items.items()]):
        ut.close()
        return "error: item not in list"
    elif count > 10000 or count < -10000:
        ut.close()
        return "error: count too big or too small"
    elif (ut.select("inventory", "user_id", wherewhat="user_id", where=id) == None):
        ut.close()
        return "error: user not in db"
    old_count = ut.select("inventory", item, wherewhat="user_id", where=id)
    ut.update("inventory", item, value=old_count + count, wherewhat="user_id", where=id)
    inv = await get_inv(id)
    ut.close()
    return inv


@app.get("/user/{id}/edit")
async def append_user(id: int, item: str, count: int):
    ut = Utils()
    if not (item in [i[1].id for i in ut.all_items.items()]):
        ut.close()
        return "error: item not in list"
    elif count > 10000 or count < -10000:
        ut.close()
        return "error: count too big or too small"
    elif (ut.select("inventory", "user_id", wherewhat="user_id", where=id) == None):
        ut.close()
        return "error: user not in db"
    ut.update("inventory", item, value=count, wherewhat="user_id", where=id, mark="+")
    inv = await get_inv(id)
    ut.close()
    return inv


@app.get("/user/{id}/get")
async def get_inv(id: int):
    ut = Utils()
    if (ut.select("inventory", "user_id", wherewhat="user_id", where=id) == None):
        ut.close()
        return "error: user not in db"
    items = [i[1].id for i in ut.all_items.items()]
    inv = ut.select("inventory", items, wherewhat="user_id", where=id)
    ut.close()
    inv = dict(zip(items, inv))
    return inv
