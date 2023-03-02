import utils
from dotenv import load_dotenv
from os import getenv
import logging
from discord_webhook_logging import DiscordWebhookHandler

load_dotenv()

formatter = logging.Formatter("[%(asctime)s] %(message)s")
all = logging.getLogger("all")
handler = DiscordWebhookHandler(
    webhook_url='https://discord.com/api/webhooks/1080850163851087942/Zj56jLLYiC7fGOM9u9un71WBLpyehKDE6ue-tVcS_IgQot12ZF936D2UiLEgVJnYoTx6')
all.addHandler(handler)
trades = logging.getLogger("trades")
handler = DiscordWebhookHandler(
    webhook_url='https://discord.com/api/webhooks/1080850018828824587/bump8Kz_uuypa40w7AY1cuOmPBLw7NkdkeDw-bFXUmT2p4FA8qVBSfXFhMGIb0Kf8u51')
trades.addHandler(handler)

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
