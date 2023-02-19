from aiogram import types
from utils import Utils
from cache import cache
ut = Utils()

#@cache()
def start_button():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Добавить бота в чат', url='http://t.me/ipanieaslabot?startgroup=hbase')
    keyboard.add(button)
    return keyboard

#@cache()
def add_inline(list):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for i in list:
        buttons.append(types.InlineKeyboardButton(text=i[0], callback_data=i[1]))
    keyboard.add(*buttons)
    return keyboard

#@cache()
def add_buttons(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

def button(inv, ut):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    endslist = ut.endslist
    itemslist = ut.itemlist
    useslist = ut.uselist
    datalist = ut.datalist
    emojilist = ut.emojilist

    for item in itemslist:
        if inv[item] != 0 and inv[useslist[itemslist.index(item)]] == 0:
            name = endslist[itemslist.index(item)][0]
            emoji = emojilist[itemslist.index(item)]
            keyboard.add(types.InlineKeyboardButton(text=f"Юзнуть {name}{emoji}",
                                                    callback_data=datalist[itemslist.index(item)]))
    return keyboard

#@cache()
def shop_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    products = ut.select("products", ["id", "name", "price"], "type", "passive", many=True)
    for i, n, p in products:
        keyboard.add(types.InlineKeyboardButton(text=f"{n} - {p} ослокоинов〽️", callback_data=i))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="shop_back"))
    return keyboard

#@cache()
def items_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    products = ut.select("products", ["id", "name", "price"], "type", "item", many=True)
    for i, n, p in products:
        keyboard.add(types.InlineKeyboardButton(text=f"{n} - {p} ослокоинов〽️", callback_data=i))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="shop_back"))
    return keyboard

#@cache()
def skins_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    products = ut.select("products", ["id", "name", "price"], "type", "skin", many=True)
    for i, n, p in products:
        keyboard.add(types.InlineKeyboardButton(text=f"{n} - {p} ослокоинов〽️", callback_data=i))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="shop_back"))
    return keyboard

#@cache()
def pass_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=f"Забрать награду", callback_data="pickup_reward"))
    return keyboard
