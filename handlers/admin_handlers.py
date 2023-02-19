from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from dp import dp, bot, Dialog
import config
from utils import *
from buttons import *
from key_generator.key_generator import generate
import os


ut = Utils()


@dp.message_handler(is_group=True, is_admin=True, commands="give")
async def give(message: types.Message):
    emoji_list = list(ut.emojilist)
    emoji_list.extend(["〽️", "🎉"])
    item_list = list(ut.itemlist)
    item_list.extend(["coins", "balance"])
    endslist = ut.endslist
    endslist.extend([["ослокоин", "ослокоина", "ослокоинов"], ["ипание", "ипания", "ипаний"]])
    chat_id = str(message.chat.id)
    usid = message.from_user.id
    text = message.get_args().split()
    if len(text) != 2:
        await message.reply(bold("Форма заполнена неправильно!\nПример: /give 💊 10"))
        return
    if not message.reply_to_message:
        await message.reply(bold("Ответь на сообщение тому, кому ты хочешь передать предмет!"))
        return
    reply_usid = message.reply_to_message.from_user.id
    if not text[0] in emoji_list:
        await message.reply("Такого предмета не существует!")
        return
    it_name = item_list[emoji_list.index(text[0])]
    try:
        int(text[1])
    except:
        await message.reply(bold("Число введено не верно."))
    if message.reply_to_message.from_user.is_bot:
        await message.reply(bold("Ты не можешь передать предмет боту!"))
        return
    user = ut.select("inventory", "user_id", "user_id", reply_usid)
    if user is None:
        await message.reply(bold("Упс! Похоже пользователь еще не играл в бота!"))
        return
    if it_name != "balance":
        ut.update("inventory", it_name, text[1], "user_id", reply_usid, "+")
    else:
        ut.update(chat_id, it_name, text[1], "user_id", reply_usid, "+")
    await message.reply(bold(f"Я успешно выдал пользователю {mention_reply(message)}, {text[1]} {ending(endslist[item_list.index(it_name)][0], endslist[item_list.index(it_name)][1], endslist[item_list.index(it_name)][2], int(text[1]))}{text[0]}!"))


@dp.message_handler(is_private=True, is_admin=True, commands="post")
async def post(message: types.Message):
    await message.reply("Введи сообщение для рассылки:", reply_markup=add_buttons(["Отмена"]))
    await Dialog.posting.set()


@dp.message_handler(state=Dialog.posting)
async def posting(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Отменено", reply_markup=types.ReplyKeyboardRemove())
        return
    ids = ut.select("private", "user_id", many=True)
    chats = ut.select("sqlite_master", "name", "type", 'table', many=True)
    print(chats)
    for table in ut.removetables:
        print(table)
        chats.remove(table)
    ids.extend(chats)
    post_count = 0
    for usid in ids:
        try:
            await bot.copy_message(usid[0], message.chat.id, message.message_id)
            post_count += 1
        except:
            pass
    await state.finish()


@dp.message_handler(is_admin=True, commands="info")
async def info(message: types.Message):
    tables_list = ut.select("sqlite_master", "name", "type", 'table', many=True)
    for table in ut.removetables:
        tables_list.remove(table)
    tables = ', '.join([str(x) for t in tables_list for x in t])
    users_list = ut.select("private", "user_id", many=True)
    users = ', '.join([str(x) for t in users_list for x in t])
    with open('newfile.txt', 'w+', encoding="utf-8") as file:
        file.write(f"Список чатов({len(tables_list)}): {tables}\n")
        file.write(f"Список пользователей({len(users_list)}): {users}\n")
        file.close()
    doc = open("newfile.txt", "rb")
    await bot.send_document(message.chat.id, doc)
    os.remove("newfile.txt")


@dp.message_handler(is_admin=True, commands="chat")
async def chat(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler(is_admin=True, commands="user")
async def user(message: types.Message):
    await message.reply(message.reply_to_message.from_user.id)


@dp.message_handler(is_admin=True, commands="setadmin")
async def setadmin(message: types.Message):
    config.add_admin(message.reply_to_message.from_user.id)
    await message.reply("Админ назначен")


@dp.message_handler(is_admin=True, commands="deladmin")
async def deladmin(message: types.Message):
    config.del_admin(message.reply_to_message.from_user.id)
    await message.reply("Админ снят")


@dp.message_handler(is_admin=True, commands="who")
async def who(message: types.Message):
    if message.reply_to_message:
        who = await bot.get_chat_member(message.reply_to_message.from_user.id, message.reply_to_message.from_user.id)
        await message.reply(who)
    else:
        text = message.get_args()
        who = await bot.get_chat_member(text, text)
        await message.reply(who)


@dp.message_handler(is_admin=True, commands="inv")
async def inv(message: types.Message):
    if message.reply_to_message:
        inv = ut.select_inventory(message, reply=True)
        await message.reply(inv)
    else:
        text = message.get_args()
        inv = ut.select_inventory(message, id=int(text))
        await message.reply(inv)


@dp.message_handler(is_admin=True, commands="clear")
async def clear(message: types.Message):
    if message.reply_to_message:
        id = message.reply_to_message.from_user.id
    else:
        id = message.get_args()

    chats = []
    infos = []
    tables = ut.select("sqlite_master", "name", "type", "table", many=True)
    for table in ut.removetables:
        tables.remove(table)
    for table in tables:
        ut.delete(table[0], "user_id", id)

    ut.delete("inventory", "user_id", id)

    await message.reply("Прогресс пользователя очищен.")


@dp.message_handler(is_admin=True, commands="reload_names")
async def test(message: types.Message):
    users = ut.select("inventory", "user_id", many=True)
    for usid in users:
        try:
            who = await bot.get_chat_member(usid[0], usid[0])
        except Exception as e:
            print(e)
            continue
        print(who.user.first_name)
        try:
            ut.update("inventory", "user_name", who.user.first_name, "user_id", usid[0])
        except Exception as e:
            print(e)


@dp.message_handler(is_admin=True, commands="genkey")
async def genkey(message: types.Message):
    text = message.get_args().split()
    if len(text) == 2:
        key = generate(5, '-', 5, 5, type_of_value='hex').get_key()
        maxuses = text[0]
        reward = text[1]
        ut.insert("keys", "key", key)
        ut.update("keys", "maxuses", maxuses, "key", key)
        ut.update("keys", "reward", reward, "key", key)
        await message.reply(f"Ключ {key} успешно сгенерирован.")


@dp.message_handler(is_admin=True, commands="delkey")
async def genkey(message: types.Message):
    text = message.get_args().split()
    if len(text) == 1:
        key = text[0]
        ut.delete("keys", "key", key)
        await message.reply(f"Ключ {key} успешно удален.")
