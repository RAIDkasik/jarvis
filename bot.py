import platform
import sqlite3
from telebot import types
import telebot
import commands

db = sqlite3.connect("db.db")
cursor = db.cursor()
token = cursor.execute(f"SELECT * FROM settings").fetchone()[0]
bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(call):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    tg = call.tg
    if "yes" in tg:
        id = tg.split(" ")[1]
        cursor.execute(f"INSERT INTO tg (id) VALUES ('{id}')")
        db.commit()
        bot.send_message(id, "Вы получили разрешение")
        bot.send_message(call.message.chat.id, f"Вы выдали разрешение, если выдали случайно, то введите `/ban {id}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    if cursor.execute(f"SELECT * FROM tg WHERE id='{message.chat.id}'").fetchone() is None:
        if cursor.execute(f"SELECT * FROM tg").fetchone() is None:
            bot.send_message(message.chat.id, "Вы успешно подключились!\nЛюбая попытка подключения к вашему Джарвису через телеграм будет приходить в этот чат")
            cursor.execute(f"INSERT INTO tg (id) VALUES ('{message.chat.id}')")
            db.commit()
        else:
            bot.send_message(message.chat.id, f"Ожидайте разрешения админа")
            id = cursor.execute(f"SELECT * FROM tg").fetchone()[0]
            bot.forward_message(id, message.chat.id, message.id)
            mar = types.InlineKeyboardMarkup()
            mar.add(types.InlineKeyboardButton(text="❌ нет", callback_tg=f"no {message.chat.id}"))
            mar.add(types.InlineKeyboardButton(text="✅ да", callback_tg=f"yes {message.chat.id}"))
            bot.send_message(id, f"Пользователь {message.from_user.first_name}, @{message.from_user.username}, {message.chat.id} пытается подключиться к Вашему Джарвису\n\nРазрешить подключенеие?", reply_markup=mar)

@bot.message_handler()
def ban(message):
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    if message.text.split(" ")[0] == "/ban":
        id = message.text.split(' ')[1]
        cursor.execute(f"DELETE FROM tg WHERE id='{id}'")
        db.commit()
        bot.send_message(id, "Админ Вас заблокировал")
        bot.send_message(message.chat.id, "Успешно!")
    else:
        if cursor.execute(f"SELECT * FROM tg WHERE id='{message.chat.id}'") is not None:
            commands.main(message.text.lower(), platform.system().lower())

bot.polling(none_stop=True)