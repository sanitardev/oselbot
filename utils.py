import sqlite3
from aiogram.utils.markdown import hlink


def mention(mess):
    first = mess.from_user.first_name
    id = mess.from_user.id
    return hlink(first, f'tg://user?id={id}')


def mention_reply(mess):
    first = mess.reply_to_message.from_user.first_name
    id = mess.reply_to_message.from_user.id
    return hlink(first, f'tg://user?id={id}')


def bold(text):
    return f"<b>{text}</b>"


def code(text):
    return f"<code>{text}</code>"


def ending(one, two, many, num):
    mod = abs(num) % 10
    num = abs(num) % 100
    if 10 < num < 20:
        form = 3
    elif mod == 1:
        form = 1
    elif 1 < mod < 5:
        form = 2
    else:
        form = 3
    if form == 1:
        return one
    elif form == 2:
        return two
    else:
        return many


# def invert(dct):
#     return dict(map(reversed, dct.items()))
class Item:
    def __init__(self, id, name, emoji, use_text, ends, chance):
        self.id = id
        self.name = name
        self.emoji = emoji
        self.use_text = use_text
        self.ends = ends
        self.chance = chance

    def use(self, chat, usid):
        Utils.update("inventory", self.id, 1, "user_id", usid, "-")
        Utils.update(chat, self.id, 1, "user_id", usid)

    def deuse(self, chat, usid):
        Utils.update(chat, self.id, 0, "user_id", usid)


class Utils:
    def __init__(self):
        self.conn = sqlite3.connect("db/database.db")
        self.cur = self.conn.cursor()
        self.conn.isolation_level = None

    def close(self):
        self.conn.close()

    removetables = [("admins",), ("inventory",), ("keys",), ("private",), ("products",)]
    oselpass = [[2, "viagra", "💊"], [5, "condoms", "🍌"], [2, "morfin", "🧪"], [3, "beer", "🍺"], [4, "vodka", "🍾"],
                [5, "viagra", "💊"], [1, "pornfilm", "🎬"], [4, "beer", "🍺"], [5, "vodka", "🍾"], [5, "viagra", "💊"],
                [3, "pornfilm", "🎬"], [5, "vodka", "🍾"], [5, "beer", "🍺"], [3, "pornfilm", "🎬"], [5, "viagra", "💊"],
                [5, "beer", "🍺"], [5, "vodka", "🍾"], [3, "pornfilm", "🎬"], [5, "beer", "🍺"], [5, "viagra", "💊"],
                [5, "vodka", "🍾"]]
    all_items = {
        "viagra": Item("viagra", "виагра", "💊", "Ты успешно заюзал виагру, и можешь снова выебать асла!",
                       ["виагру", "виагры", "виагр"], 20),
        "vodka": Item("vodka", "водка", "🍾", "Ты успешно выпил водку, и можешь выебать асла в 2 раза больше!",
                      ["водку", "водки", "водок"], 20),
        "beer": Item("beer", "пиво", "🍺", "Ты успешно выпил пиво, и теперь асел не может тебя отпиздить!",
                     ["пиво", "пива", "пива"], 30),
        "condoms": Item("condoms", "презерватив", "🍌",
                        "Ты успешно заюзал презерватив, и теперь пиздюлей асла стало меньше!",
                        ["презерватив", "презерватива", "презервативов"], 50),
        "pornfilm": Item("pornfilm", "порно-фильм", "🎬",
                         "Ты успешно заюзал порно-фильм, и можешь выебать асла в 5 раз больше!",
                         ["порно-фильм", "порно-фильма", "порно-фильмов"], 10),
        "morfin": Item("morfin", "морфин", "🧪",
                       "Ты успешно заюзал морфин, и если асел тебя отпиздит, задержка сброситься!",
                       ["морфин", "морфина", "морфинов"], 20),
        "heal": Item("heal", "лечебная мазь", "🧴", "Ты успешно заюзал мазь, и у асла вылечилось очко!",
                     ["лечебную мазь", "лечебные мази", "лечебных мазей"], 20),
    }
    itemlist = [i.id for i in all_items.values()]
    itemnamelist = [i.name for i in all_items.values()]
    emojilist = [i.emoji for i in all_items.values()]
    endslist = [i.ends for i in all_items.values()]
    textslist = [i.use_text for i in all_items.values()]
    chancelist = [i.chance for i in all_items.values()]
    tableslist = []
    tableslist.extend(itemlist)
    tableslist.extend(
        ["bonus_time", "coins", "whip", "whip_use", "energy", "dildo", "reward_lvl", "osel_counter", "reward", "skin",
         "vitamine", "vibrator"])
    uselist = [i + "_use" for i in itemlist]
    datalist = ["use_" + i for i in itemlist]

    skin_stickers = {
        "skin0": "CAACAgIAAxkBAAEHZb9jzqSaToUoUJi0EOuMgxWzsoJ9xAAC-iMAAgLkeEqIUzZx6VLkIC0E",
        "skin1": "CAACAgIAAxkBAAEHZcFjzqSc24w2kIwWNOEvm3-Glz9T2QACTycAAtFIcUolCn39IKd6ey0E",
        "skin2": "CAACAgIAAxkBAAEHZcNjzqTB2woe9vNzgofzhBulE9VLxQACyyMAAtg1cUo_kNV90H9CPS0E",
        "skin3": "CAACAgIAAxkBAAEHZcVjzqTEowoLN2UXMYbFyloexG9F1QACG1EAAm5ceUqkuHV90NJTli0E",
        "skin4": "CAACAgIAAxkBAAEHZcdjzqTFgTW6k_jm-C5Cbfb0d5DongAC3SgAAri6eEoUM9EL6OQY8i0E",
        "skin5": "CAACAgIAAxkBAAEHZcljzqTHGAddwXB7sBf-jrN6pJF42AACbyYAAqb8eUrJfsAZsTEIxy0E"
    }

    def create_table(self, msg):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "{msg.chat.id}" (
				"user_id"	INTEGER NOT NULL UNIQUE,
				"balance"	INTEGER NOT NULL DEFAULT (0),  
				"time"	INTEGER NOT NULL DEFAULT (0)
			)''')
        try:
            self.cur.execute(f"ALTER TABLE '{msg.chat.id}' ADD COLUMN 'break' INTEGER DEFAULT 0")
        except:
            pass
        for table in self.tableslist:
            try:
                self.cur.execute(f"ALTER TABLE inventory ADD COLUMN '{table}' INTEGER DEFAULT 0")
            except:
                pass
        for use in self.uselist:
            try:
                self.cur.execute(f"ALTER TABLE '{msg.chat.id}' ADD COLUMN '{use}' INTEGER DEFAULT 0")
            except:
                pass
        try:
            self.cur.execute(f"ALTER TABLE inventory ADD COLUMN 'skin_list' TEXT DEFAULT 'skin0'")
        except:
            pass
        self.insert("inventory", "user_id", msg.from_user.id)
        self.insert(str(msg.chat.id), "user_id", msg.from_user.id)
        self.update("inventory", "user_name", msg.from_user.first_name, "user_id", msg.from_user.id)

    def insert(self, table, column, value):
        if isinstance(column, list) and isinstance(value, list):
            values = ""
            for val in value:
                values += f"'{val}', "
            self.cur.execute(f"INSERT OR IGNORE INTO '{table}'({', '.join(map(str, column))}) VALUES({value})")
        else:
            self.cur.execute(f"INSERT OR IGNORE INTO '{table}'({column}) VALUES('{value}')")

    def update(self, table, column, value, where, wherewhat, mark=None):
        if mark is not None:
            self.cur.execute(f"UPDATE '{table}' SET {column} = {column} {mark} '{value}' WHERE {where} = '{wherewhat}'")
        else:
            self.cur.execute(f"UPDATE '{table}' SET {column} = '{value}' WHERE {where} = '{wherewhat}'")

    def select(self, table, column, wherewhat=None, where=None, many=False):

        if isinstance(column, list):
            request = f"SELECT {', '.join(map(str, column))} FROM '{table}'"
        else:
            request = f"SELECT {column} FROM '{table}'"
        if wherewhat is not None:
            request += f" WHERE {wherewhat} = '{where}'"
        self.cur.execute(request)
        try:
            if many:
                res_select = self.cur.fetchall()
            else:
                res_select = self.cur.fetchone()
                if len(res_select) < 2:
                    res_select = res_select[0]
                else:
                    res_select = res_select
        except:
            res_select = None
        return res_select

    def delete(self, table, where=None, wherewhat=None):
        request = f"""DELETE FROM '{table}'"""
        if where is not None:
            request += f" WHERE {where} = '{wherewhat}'"
        self.cur.execute(request)

    def insert_to_private(self, msg):
        self.insert("private", "user_id", msg.from_user.id)

    def select_top(self, table):
        self.cur.execute(f"SELECT user_id, balance FROM '{table}' ORDER BY balance DESC LIMIT 10")
        try:
            res_select = self.cur.fetchall()
        except:
            res_select = None
        return res_select

    def select_inventory(self, msg=None, reply=None, call=None, id=None, chat=None):
        inventory = {}
        if id is not None and chat is not None:
            usid = id
            chat = chat
        else:
            usid = msg.from_user.id
            if call:
                chat = msg.message.chat.id
            else:
                chat = msg.chat.id
            if reply:
                usid = msg.reply_to_message.from_user.id
        tables = self.tableslist
        tables.append("skin")
        for table in tables:
            inventory[table] = self.select("inventory", table, "user_id", usid)
        chat_tables = ["timer", "balance"]
        chat_tables.extend(self.uselist)
        for table in chat_tables:
            if table == "timer":
                inventory[table] = self.select(str(chat), "time", "user_id", usid)
            else:
                inventory[table] = self.select(str(chat), table, "user_id", usid)
        inventory["break"] = self.select(str(chat), "break", "user_id", usid)
        return inventory

    def select_globaltop(self):
        chats = []
        infos = []
        tables = self.select("sqlite_master", "name", "type", "table", many=True)
        for table in self.removetables:
            tables.remove(table)
        for table in tables:
            chats.append(table[0])
        for chat in chats:
            info = self.select(chat, ["user_id", "balance"], many=True)
            if info is None:
                return None
            for inf in info:
                infos.append(inf)

        def key_func(item):
            return item[1]

        infos.sort(key=key_func, reverse=True)
        return infos[:10]
