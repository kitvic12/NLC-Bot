from api import bot
from telebot import types
from config import config
from admins import load_admin
from user_activity import activity_tracker

def resp():
    resp = "Список админов:\n"
    admins = load_admin()
    count = 0
    for admin in admins:
        count +=1
        resp += f"{count} - @{admin}\n"
    resp += "\n Что вы хотите сделать?"
    return resp



@bot.message_handler(func=lambda message:message.from_user.id == config["owner_id"], commands=["admins"])
def amdin_list_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_message(config["owner_id"], resp(), reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Добавить пользователя", callback_data="admin add"), types.InlineKeyboardButton("Удалить пользователя", callback_data="admin remove")]]
    ))
