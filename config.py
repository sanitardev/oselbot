import utils
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()

ut = utils.Utils()

admin_ids = [int(x) for t in ut.select("admins", "user_id", many=True) for x in t]
ban_ids = [1087968824, 136817688, 777000]
token = getenv("TOKEN")


def add_admin(user_id):
    global admin_ids
    ut.insert("admins", "user_id", user_id)
    admin_ids = [int(x) for t in ut.select("admins", "user_id", many=True) for x in t]
    logging.warn(admin_ids)


def del_admin(user_id):
    global admin_ids
    ut.delete("admins", "user_id", user_id)
    admin_ids = [int(x) for t in ut.select("admins", "user_id", many=True) for x in t]
    logging.warn(admin_ids)
