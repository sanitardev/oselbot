from fastapi import FastAPI
from utils import *
from key_generator.key_generator import generate
import random

app = FastAPI()


# 5040607409:AAFGxAr_-1qwa-SbMXGI-i8aQfKiJVn_Aos
@app.get("/genkey")
def genkey():
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
    return f"{key}"
