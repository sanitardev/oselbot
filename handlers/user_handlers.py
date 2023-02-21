from dp import dp, rate_limit
from utils import *
from aiogram.dispatcher.filters import Text
from buttons import *
import random
from time import time
from collections import Counter
import re
from aiogram import md

ut = Utils()


@rate_limit(2, "start")
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        ut.insert_to_private(message)
        text = "С моими командами, можно ознокомится командой — /help."
    else:
        text = "Чтобы начать играть используй команду — /osel."
    await message.reply(bold(f"""Приветствую тебя, я — развлекательный бот для групп.
{text}"""), reply_markup=start_button())


async def random_ipaniy(usid, chat):
    start = time()
    inventory = ut.select_inventory(id=usid, chat=chat)
    mutliplier = 0
    if inventory["vibrator"] == 1:
        luck_chance = [30, 70]
    else:
        luck_chance = [50, 50]
    if random.choices([0, 1], luck_chance, k=1)[0] == 1:
        randomik = random.randint(0, 10)
    else:
        randomik = random.randint(-5, 0)
    if inventory["vodka_use"] == 1:
        mutliplier += 2
        ut.update(chat, "vodka_use", 0, "user_id", usid)
    if inventory["whip"] == 1:
        if inventory["whip_use"] < 10:
            randomik = abs(randomik)
            ut.update("inventory", "whip_use", 1, "user_id", usid, "+")
        else:
            ut.update("inventory", "whip", 0, "user_id", usid)
            ut.update("inventory", "whip_use", 0, "user_id", usid)
    if inventory["dildo"] == 1:
        mutliplier += 2
    if inventory["beer_use"] == 1:
        randomik = abs(randomik)
        ut.update(chat, "beer_use", 0, "user_id", usid)
    if inventory["condoms_use"] == 1:
        ut.update(chat, "condoms_use", 0, "user_id", usid)
        if randomik < 0:
            randomik += int(abs(randomik / 2))
    if inventory["pornfilm_use"] == 1:
        ut.update(chat, "pornfilm_use", 0, "user_id", usid)
        mutliplier += 5
    if mutliplier != 0:
        randomik *= mutliplier

    ut.update(chat, "balance", randomik, "user_id", usid, "+")
    balance = ut.select(chat, "balance", "user_id", usid)

    if randomik < 0:
        text = f"твой асел уипал тебя, и забрал {abs(randomik)} {ending('ипание', 'ипания', 'ипаний', randomik)}."
    elif randomik > 0:
        text = f"тебе удалось выипать асла {randomik} {ending('раз', 'раза', 'раз', randomik)}."
    else:
        text = f"у тебя не получилось выипать асла."
    stop = time() - start
    return text, balance, randomik



async def is_break(usid, chat):
    start = time()
    inventory = ut.select_inventory(id=usid, chat=chat)
    breaks = random.choices([False, True], [100, 10], k=1)[0]
    if breaks:
        ut.update(chat, "break", 1, "user_id", usid)
        if inventory["vitamine"] == 1:
            text = "У осла разорвалось очко, и ты не можешь его ипать 2 часа!"
        else:
            text = "У осла разорвалось очко, и ты не можешь его ипать 4 часа!"
    else:
        text = "Следующая попытка через час!"
    stop = time() - start
    return text, breaks


async def random_item(usid, chat):
    start = time()
    inventory = ut.select_inventory(id=usid, chat=chat)
    chancelist = ["", "coins"]
    chancelist.extend(ut.itemlist)
    nameslist = ["", ["оселкоин", "оселкоина", "оселкоинов"]]
    nameslist.extend(ut.endslist)
    chance = random.choices(chancelist, [40 if inventory["vibrator"] == 1 else 80, 40] + ut.chancelist, k=1)[0]
    if chance != "":
        itemrandom = random.randint(1, 3)
        ut.update("inventory", chance, itemrandom, "user_id", usid, "+")
        idlist = chancelist.index(chance)
        stop = time() - start
        return [itemrandom, ending(nameslist[idlist][0], nameslist[idlist][1], nameslist[idlist][2], itemrandom)]
    stop = time() - start
    return False, False


async def handle_delay(usid, chat):
    start = time()
    inventory = ut.select_inventory(id=usid, chat=chat)
    if inventory["viagra_use"] == 1:
        ut.update(chat, "time", 0, "user_id", usid)
        ut.update(chat, "viagra_use", 0, "user_id", usid)
    if inventory["heal_use"] == 1:
        ut.update(chat, "time", 0, "user_id", usid)
        ut.update(chat, "heal_use", 0, "user_id", usid)
        ut.update(chat, "break", 0, "user_id", usid)
    inventory = ut.select_inventory(id=usid, chat=chat)
    timer = inventory["timer"]
    if not timer == 0:
        if int(timer) - int(time()) <= 0:
            ut.update(chat, "time", 0, "user_id", usid)
            ut.update(chat, "break", 0, "user_id", usid)
            stop = time() - start
            return False
        else:
            stop = time() - start
            return await time_parse(timer)
    else:
        stop = time() - start
        return False


async def set_delay(usid, chat, randomik):
    inventory = ut.select_inventory(id=usid, chat=chat)
    times = int(time()) + 3600
    start = time()
    if inventory["break"] != 1:
        if inventory["energy"] == 1:
            times = int(time()) + 1800
        ut.update(chat, "time", times, "user_id", usid)
        if inventory["morfin_use"] == 1:
            ut.update(chat, "morfin_use", 0, "user_id", usid)
            if randomik < 0:
                ut.update(chat, "time", 0, "user_id", usid)
    else:
        if inventory["vitamine"] == 1:
            ut.update(chat, "time", int(time()) + 7200, "user_id", usid)
        else:
            ut.update(chat, "time", int(time()) + 14400, "user_id", usid)
    stop = time() - start

async def time_parse(timer):
    start = time()
    sec = int(timer) - int(time())
    mins = int(sec / 60)
    hours = int(mins / 60)
    mins = int(mins % 60)
    if not hours == 0:
       text = f"Приходи через {hours} {ending('час', 'часа', 'часов', hours)} {mins} {ending('минуту', 'минуты', 'минут', mins)}."
    else:
        if not mins == 0:
           text = f"Приходи через {mins} {ending('минуту', 'минуты', 'минут', mins)}."
        else:
            text = f"Приходи через {sec} {ending('секунду', 'секунды', 'секунд', sec)}."
    stop = time() - start
    return text


@rate_limit(2, "osel")
@dp.message_handler(Text(["osel", "асёл", "асел", "осел", "осёл", "аслина", "ослина"], ignore_case=True), is_group=True, is_ban=False)
@dp.message_handler(is_group=True, is_ban=False, commands=['osel', 'asel'])
async def osel(message: types.Message):
    chat = str(message.chat.id)
    usid = message.from_user.id
    ut.create_table(message)
    inventory = ut.select_inventory(message)

    skin_id = inventory['skin']
    skin = ut.skin_stickers["skin" + str(skin_id)]
    await message.reply_sticker(sticker=skin)

    delay = await handle_delay(usid, chat)
    if delay:
        viagra_text = delay
        await message.reply(bold(viagra_text), reply_markup=button(inventory, ut))
        return

    inventory = ut.select_inventory(message)

    text, balance, randomik = await random_ipaniy(usid, chat)

    viagra_text, breaks = await is_break(usid, chat)

    itemrandom, ending_string = await random_item(usid, chat)
    if itemrandom and ending_string is not False:
        viagra_text += f'\nТы получил {itemrandom} {ending_string}!'

    if inventory["reward_lvl"] != len(ut.oselpass):
        ut.update("inventory", "osel_counter", 1, "user_id", usid, "+")
        inventory = ut.select_inventory(message)
        if inventory["osel_counter"] >= 5:
            ut.update("inventory", "reward_lvl", 1, "user_id", usid, "+")
            ut.update("inventory", "osel_counter", 0, "user_id", usid)

    await message.reply(bold(f"""{mention(message)}, {text}
Теперь у тебя {balance} {ending("ипание", "ипания", "ипаний", balance)}.
{viagra_text}"""), reply_markup=button(inventory, ut))
    await set_delay(usid, chat, randomik)



@rate_limit(2, "bonus")
@dp.message_handler(Text(["Бонус", "Bonus"], ignore_case=True), is_group=True, is_ban=False)
@dp.message_handler(is_group=True, is_ban=False, commands=['bonus'])
async def bonus(message: types.Message):
    chat = str(message.chat.id)
    usid = message.from_user.id
    times = int(time()) + 86400
    text = ""
    bonus_list = ["", "coins", "balance"]
    bonus_list.extend(ut.itemlist)
    names_list = ["", ["оселкоин", "оселкоина", "оселкоинов"], ["ипание", "ипания", "ипаний"]]
    names_list.extend(ut.endslist)
    emoji_list = ["", "〽️", "🎉"]
    emoji_list.extend(ut.emojilist)
    ut.create_table(message)
    ut.insert(chat, "user_id", usid)
    inventory = ut.select_inventory(message)
    timer = inventory["bonus_time"]
    if not timer == 0:
        if int(timer) - int(time()) <= 0:
            ut.update("inventory", "bonus_time", 0, "user_id", usid)
        else:
            await message.reply(bold(await time_parse(timer)))
            return
    bonus = random.choices(bonus_list, [35 if inventory["vibrator"] == 1 else 70, 40, 30] + ut.chancelist, k=3)
    bonlist = []
    for bon in bonus:
        if bon == "":
            continue
        bonlist.append(bon)
        count = random.randint(1, 4)
        id_bonus = bonus_list.index(bon)
        cnt = Counter(bonlist)
        if cnt[bon] > 1:
            continue
        try:
            ut.update("inventory", bon, count, "user_id", usid, "+")
        except:
            ut.update(chat, bon, count, "user_id", usid, "+")
        text += f'\n• {count} {ending(names_list[id_bonus][0], names_list[id_bonus][1], names_list[id_bonus][2], count)}{emoji_list[id_bonus]}'
    if text == "":
        text = "\n• Ничего! В следующий раз повезет."
    await message.reply(bold(f"Твой ежедневный бонус:{text}\n\nПриходи завтра!"))
    ut.update("inventory", "bonus_time", times, "user_id", usid)


@rate_limit(2, "top")
@dp.message_handler(Text(["Рейтинг", "Топ", "Top"], ignore_case=True), is_group=True)
@dp.message_handler(is_group=True, commands="top")
async def top(message: types.Message):
    chat = str(message.chat.id)
    usid = message.from_user.id
    top = ""
    num = 2
    ut.create_table(message)
    info = ut.select_top(chat)
    try:
        best = info.pop(0)
        for us in info:
            user_id, count = us
            try:
                name = ut.select("inventory", "user_name", "user_id", user_id)
            except:
                continue
            top += f"{num}. {md.quote_html(name)} — {count} {ending('ипание', 'ипания', 'ипаний', count)}.\n"
            num += 1
        best_id, best_count = best
        try:
            best_name = ut.select("inventory", "user_name", "user_id", best_id)
        except:
            best_name = None
        best = f"👑 {md.quote_html(best_name)} — {best_count} {ending('ипание', 'ипания', 'ипаний', best_count)}.\n"
    except:
        best, top = ["", ""]
    await message.reply(bold(f"Топ 10 людей по количеству ипаний.\n{best}{top}"))


@rate_limit(2, "globaltop")
@dp.message_handler(Text(["Глобальный топ", "Глобальный рейтинг", "Глобалтоп", "Глобал топ", "Globaltop", "Global top"],
                         ignore_case=True), is_group=True)
@dp.message_handler(is_group=True, commands="globaltop")
async def globaltop(message: types.Message):
    top = ""
    num = 2
    info = ut.select_globaltop()
    best = info.pop(0)
    for us in info:
        user_id, count = us
        try:
            name = ut.select("inventory", "user_name", "user_id", user_id)
        except:
            continue
        top += f"{num}. {md.quote_html(name)} — {count} {ending('ипание', 'ипания', 'ипаний', count)}.\n"
        num += 1
    best_id, best_count = best
    try:
        best_name = ut.select("inventory", "user_name", "user_id", best_id)
    except:
        best_name = None
    best = f"👑 {md.quote_html(best_name)} — {best_count} {ending('ипание', 'ипания', 'ипаний', best_count)}.\n"
    await message.reply(bold(f"Глобальный топ 10 людей по количеству ипаний.\n{best}{top}"))


@rate_limit(2, "help")
@dp.message_handler(Text(["Help", "Помощь"], ignore_case=True))
@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.reply(bold(f"""Мои команды:
/start — начать
/osel — выипать асла
/use — юзнуть предмет
/pass - асел пасс
/bonus — ежедневный бонус
/trade (предмет) (количество) — передача предметов
/shop — магазин
/stat — статистика
/top — топ 10 людей по ипанию
/globaltop - глобальный топ 10 людей по ипанию
/usekey (ключ) - использовать промо-ключ"""))


@rate_limit(2, "stat")
@dp.message_handler(Text(["Statistics", "Stat", "Стат", "Стата", "Статистика"], ignore_case=True), is_group=True, is_ban=False)
@dp.message_handler(is_group=True, is_ban=False, commands=["stat", "statistics"])
async def stat(message: types.Message):
    chat = str(message.chat.id)
    usid = message.from_user.id
    inv = ""
    ut.create_table(message)
    ut.insert(chat, "user_id", usid)
    inventory = ut.select_inventory(message)
    coins = inventory["coins"]
    balance = inventory["balance"]
    items = ut.itemlist
    emoji = ut.emojilist
    endings = ut.endslist
    for item in items:
        if inventory[item] != 0:
            inv += f"• {inventory[item]} {ending(ut.itemnamelist[items.index(item)], endings[items.index(item)][1], endings[items.index(item)][2], inventory[item])}{emoji[items.index(item)]}\n"
    if inv == "":
        inv = "• Пуст"

    skin_id = inventory['skin']
    skin = ut.skin_stickers["skin" + str(skin_id)]
    await message.reply_sticker(sticker=skin)

    await message.reply(bold(f"""Статистика {mention(message)}:

Кол-во ипаний асла🎉
• {balance}

Кол-во ослокоинов〽️
• {coins}

Инвентарь:
{inv}"""))


@rate_limit(2, "trade")
@dp.message_handler(is_group=True, is_ban=False, commands="trade")
async def trade(message: types.Message):
    if message.chat.type == 'private':
        await message.reply("Меня можно юзать только в чатах!", reply_markup=start_button())
        return
    emoji_list = list(ut.emojilist)
    emoji_list.append("〽️")
    item_list = list(ut.itemlist)
    item_list.append("coins")
    endslist = ut.endslist
    endslist.append(["ослокоин", "ослокоина", "ослокоинов"])
    chat = str(message.chat.id)
    usid = message.from_user.id
    text = message.get_args().split()
    if len(text) != 2:
        await message.reply(bold("Форма заполнена неправильно!\nПример: /trade 💊 10"))
        return
    if not message.reply_to_message:
        await message.reply(bold("Ответь на сообщение тому, кому ты хочешь передать предмет!"))
        return
    reply_usid = message.reply_to_message.from_user.id
    if not text[0] in emoji_list:
        await message.reply("Такого предмета не существует!")
        return
    if reply_usid == usid:
        await message.reply(bold("Ты не можешь передать предмет самому себе!"))
        return
    it_name = item_list[emoji_list.index(text[0])]
    item = ut.select("inventory", it_name, "user_id", usid)

    try:
        if int(text[1]) < 0:
            await message.reply(bold("Число введено не верно."))
            return
        if int(text[1]) > item:
            await message.reply(bold("У тебя недостаточно количества предмета!"))
            return
    except:
        await message.reply(bold("Число введено не верно."))
        return
    if message.reply_to_message.from_user.is_bot:
        await message.reply(bold("Ты не можешь передать предмет боту!"))
        return
    user = ut.select("inventory", it_name, "user_id", reply_usid)
    if user == None:
        await message.reply(bold("Упс! Похоже пользователь еще не играл в бота!"))
        return
    ut.update("inventory", it_name, text[1], "user_id", reply_usid, "+")
    ut.update("inventory", it_name, text[1], "user_id", usid, "-")
    await message.reply(bold(
        f"Я успешно передал пользователю {mention_reply(message)}, {text[1]} {ending(endslist[item_list.index(it_name)][0], endslist[item_list.index(it_name)][1], endslist[item_list.index(it_name)][2], int(text[1]))}{text[0]}!"))


@rate_limit(2, "shop")
@dp.message_handler(is_group=True, commands="shop")
async def shop(message: types.Message):
    await message.reply(bold("► Магазин🏪 ◄"),
                        reply_markup=add_inline([["Предметы", "passive"], ["Скины", "skins"], ["Расходники", "items"]]))


@dp.callback_query_handler(text=["passive", "skins", "items", "shop_back"])
async def shop_handler(call: types.CallbackQuery):
    if call.data == "passive":
        await call.message.edit_text(bold("""► Магазин Предметов🏪 ◄
Дилдо - навсегда умножает ипания или пиздюли на 2.
Плеть - 10 раз сдерживает пиздюли асла, потом исчезает.
Энергетик - задержка между ипаниями пол часа.
Витамины - задержка после разрыва очка 2 часа, вместо 4.
Вибратор - повышает удачу."""), reply_markup=shop_button())
    elif call.data == "skins":
        await call.message.edit_text(bold("""► Магазин Скинов🏪 ◄"""), reply_markup=skins_button())
    elif call.data == "items":
        await call.message.edit_text(bold("""► Магазин Расходников🏪 ◄"""), reply_markup=items_button())
    elif call.data == "shop_back":
        await call.message.edit_text(bold("► Магазин🏪 ◄"), reply_markup=add_inline(
            [["Предметы", "passive"], ["Скины", "skins"], ["Расходники", "items"]]))


@rate_limit(2, "use")
@dp.message_handler(Text(["Юз", "Use", "заюзать"], ignore_case=True), is_group=True, is_ban=False)
@dp.message_handler(is_group=True, is_ban=False, commands="use")
async def use(message: types.Message):
    ut.create_table(message)
    try:
        text = message.get_args().split()
    except:
        text = []
    usid = message.from_user.id
    chat = message.chat.id
    emoji = ut.emojilist
    items = ut.itemlist
    uses = ut.uselist
    inventory = ut.select_inventory(message)
    if text == []:
        await message.reply(bold("""💊 Виагра — пропускает задержку между ипаниями.
🍾 Водка — увеличивает ипания/пиздюли в 2 раза.
🍺 Пиво — сдерживает пиздюли асла.
🍌 Презерватив — уменьшает боль от пиздюлей.
🎬 Порно-фильм — увеличивает ипания/пиздюли в 5 раз.
🧪 Морфин - если асел тебя отпиздит, задержка сброситься.
🧴 Лечебная мазь - лечит очко асла.

Что-бы использовать предмет, используй команду /use [смайлик предмета]"""))
    else:
        if len(text) != 1:
            await message.reply(bold("Неверно заполнена форма!"))
            return
        text = text[0]
        if not text in emoji:
            await message.reply(bold("Такого предмета не существует!"))
            return
        if inventory[items[emoji.index(text)]] == 0:
            await message.reply(bold("У тебя нет такого предмета!"))
            return
        if inventory[uses[emoji.index(text)]] != 0:
            await message.reply(bold("У тебя и так использован этот предмет!"))
            return
        if uses[emoji.index(text)] == "viagra_use" and inventory["break"] == 1:
            await message.reply(bold("У асла разорвано очко!"))
            return
        if uses[emoji.index(text)] == "heal_use" and inventory["break"] == 0:
            await message.reply(bold("У асла не разорвано очко!"))
            return
        ut.update("inventory", items[emoji.index(text)], 1, "user_id", usid, "-")
        ut.update(chat, uses[emoji.index(text)], 1, "user_id", usid)
        await message.reply(bold("Ты успешно заюзал предмет!"))


@rate_limit(2, "pass")
@dp.message_handler(is_group=True, is_ban=False, commands="pass")
async def oselpass(message: types.Message):
    usid = message.from_user.id
    ut.create_table(message)
    inv = ut.select_inventory(message)
    if inv["osel_counter"] >= 5:
        ut.update("inventory", "reward_lvl", 1, "user_id", usid, "+")
        ut.update("inventory", "osel_counter", 0, "user_id", usid)
    inv = ut.select_inventory(message)
    if inv["reward_lvl"] != len(ut.oselpass):
        await message.reply_photo(open("images/oselpass.png", 'rb'), bold(f"""► Асел пасс 🎫 ◄
Уровень: {inv["reward_lvl"]}
Доступно наград: {inv["reward_lvl"] - inv["reward"]}
Попыток ипаний до следуещего уровня: {5 - inv['osel_counter']}"""), reply_markup=pass_button())
    else:
        await message.reply_photo(open("images/oselpass.png", 'rb'), bold(f"""► Асел пасс 🎫 ◄
Уровень: {inv["reward_lvl"]}
Доступно наград: {inv["reward_lvl"] - inv["reward"]}
Аселпасс пройден!"""), reply_markup=pass_button())


@dp.callback_query_handler(text="pickup_reward")
async def pass_callback(call: types.CallbackQuery):
    try:
        if not call.message.reply_to_message.from_user.id == call.from_user.id:
            return
    except:
        return
    usid = call.from_user.id
    inv = ut.select_inventory(call, call=True)
    if inv["reward_lvl"] - inv["reward"] != 0:
        ut.update("inventory", "reward", 1, "user_id", usid, "+")
        inv = ut.select_inventory(call, call=True)
        reward = inv["reward"] - 1
        rewards = ut.oselpass[reward]
        ut.update("inventory", rewards[1], rewards[0], "user_id", usid, "+")
        await call.answer(text=f"Ты получил {rewards[0]}{rewards[2]}!", show_alert=True)
        if inv["reward_lvl"] != len(ut.oselpass):
            await call.message.edit_caption(bold(f"""► Асел пасс 🎫 ◄
Уровень: {inv["reward_lvl"]}
Доступно наград: {inv["reward_lvl"] - inv["reward"]}
Попыток ипаний до следуещего уровня: {5 - inv['osel_counter']}"""), reply_markup=pass_button())
        else:
            await call.message.edit_caption(bold(f"""► Асел пасс 🎫 ◄
Уровень: {inv["reward_lvl"]}
Доступно наград: {inv["reward_lvl"] - inv["reward"]}
Аселпасс пройден!"""), reply_markup=pass_button())
    else:
        await call.answer(text=f"Ты не можешь забрать награду!", show_alert=True)


@rate_limit(2, "usekey")
@dp.message_handler(is_group=True, is_ban=False, commands="usekey")
async def usekey(message: types.Message):
    usid = message.from_user.id
    chatid = str(message.chat.id)
    ut.create_table(message)
    emoji_list = list(ut.emojilist)
    emoji_list.extend(["〽️", "🎉"])
    item_list = list(ut.itemlist)
    item_list.extend(["coins", "balance"])
    text = message.get_args().split()
    if len(text) == 1:
        key = text[0]
        max_uses = ut.select("keys", "maxuses", "key", key)
        if max_uses == None:
            await message.reply(bold("Ключ неверный!"))
            return
        uses = ut.select("keys", "uses", "key", key)
        reward = re.split(r'_', ut.select("keys", "reward", "key", key))
        blacklist = ut.select("keys", "blacklist", "key", key)
        if blacklist is None:
            blacklist = "0000000_"
        if uses < max_uses:
            if str(usid) in re.split(r'_', blacklist):
                await message.reply(bold("Ты уже использовал промокод!"))
                return
            ut.update("keys", "uses", 1, "key", key, "+")
            ut.update("keys", "blacklist", blacklist + (str(usid) + "_"), "key", key)
            if not reward[1] == "balance":
                ut.update("inventory", reward[1], reward[0], "user_id", usid, "+")
            else:
                ut.update(chatid, reward[1], reward[0], "user_id", usid, "+")
            await message.reply(
                bold(f"Ключ успешно использован! Награда {reward[0]} {emoji_list[item_list.index(reward[1])]}."))
        else:
            await message.reply(bold("Количество использований исчерпано!"))
    else:
        await message.reply(bold("Ключ не введен!"))


@dp.callback_query_handler()
async def use(call: types.CallbackQuery):
    chat = str(call.message.chat.id)
    usid = call.from_user.id
    products = [str(x) for t in ut.select("products", "id", "type", "passive", many=True) for x in t]
    skins = [str(x) for t in ut.select("products", "id", "type", "skin", many=True) for x in t]
    items = [str(x) for t in ut.select("products", "id", "type", "item", many=True) for x in t]
    useslist = ut.uselist
    itemlist = ut.itemlist
    uselist = ut.datalist
    textslist = ut.textslist
    user = ut.select("inventory", "user_id", "user_id", usid)
    if user == None:
        return
    if call.data in products:
        item = ut.select("inventory", call.data, "user_id", usid)
        if item == None:
            return
        coins = ut.select("inventory", "coins", "user_id", usid)
        price = ut.select("products", "price", "id", call.data)
        if item == 1:
            await call.answer(text="У тебя уже куплен этот предмет!", show_alert=True)
            return
        if coins >= price:
            ut.update("inventory", "coins", price, "user_id", usid, "-")
            ut.update("inventory", call.data, 1, "user_id", usid)
            await call.answer(text="Ты успешно купил этот предмет!", show_alert=True)
        else:
            await call.answer(text="У тебя нет столько ослокоинов!", show_alert=True)
            return
    elif call.data in skins:
        skinid = skins.index(call.data)
        coins = ut.select("inventory", "coins", "user_id", usid)
        price = ut.select("products", "price", "id", call.data)
        skin_list = ut.select("inventory", "skin_list", "user_id", usid)
        current_skin = ut.select("inventory", "skin", "user_id", usid)
        if call.data in re.split(r'_', skin_list):
            ut.update("inventory", "skin", skinid, "user_id", usid)
            await call.answer(text="Ты успешно надел этот скин!", show_alert=True)
            return
        if coins >= price:
            ut.update("inventory", "coins", price, "user_id", usid, "-")
            ut.update("inventory", "skin", skinid, "user_id", usid)
            ut.update("inventory", "skin_list", skin_list + f"_{call.data}", "user_id", usid)
            await call.answer(text="Ты успешно купил этот скин!", show_alert=True)
        else:
            await call.answer(text="У тебя нет столько ослокоинов!", show_alert=True)
            return
    elif call.data in items:
        coins = ut.select("inventory", "coins", "user_id", usid)
        price = ut.select("products", "price", "id", call.data)
        if coins >= price:
            ut.update("inventory", "coins", price, "user_id", usid, "-")
            ut.update("inventory", call.data, 1, "user_id", usid, "+")
            await call.answer(text="Ты успешно купил этот предмет!", show_alert=True)
        else:
            await call.answer(text="У тебя нет столько ослокоинов!", show_alert=True)
            return
    elif call.data in uselist:
        try:
            if not call.message.reply_to_message.from_user.id == call.from_user.id:
                return
        except:
            return
        inventory = ut.select_inventory(call, call=True)
        idlist = uselist.index(call.data)
        if not inventory[itemlist[idlist]] == 0:
            if call.data == "use_viagra" and inventory["break"] == 1:
                if inventory["heal_use"] == 0:
                    await call.answer(text="У асла разорвано очко!", show_alert=True)
                    return
            if call.data == "use_heal" and inventory["break"] == 0:
                await call.answer(text="У асла не разорвано очко!", show_alert=True)
                return
            if inventory[useslist[idlist]] == 0:
                ut.update("inventory", itemlist[idlist], 1, "user_id", usid, "-")
                ut.update(chat, useslist[idlist], 1, "user_id", usid)
                inventory = ut.select_inventory(call, call=True)
                await call.message.edit_text(f"***{textslist[idlist]}***", reply_markup=button(inventory, ut),
                                             parse_mode="Markdown")
            else:
                await call.answer(text="Ты и так заюзал этот предмет!", show_alert=True)
        else:
            await call.answer(text="У тебя нет этого предмета!", show_alert=True)
