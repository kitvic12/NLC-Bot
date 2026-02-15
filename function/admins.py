from core.api import bot
from telebot import types
from core.config import config
from core.log import log
from core.user_activity import activity_tracker
from core.database import user

import pickle

FILE_PATH3 = "admin.pkl"


#load

def load_admin():
    try:
        with open(FILE_PATH3, 'rb') as file:
            return set(pickle.load(file))
    except FileNotFoundError:
        return set()

admins = load_admin()

def save_admins(admins):
    with open(FILE_PATH3, 'wb') as file:
        pickle.dump(set(admins), file)

def admin_add(username):
        admins.add(username)
        save_admins(admins)
        log(f"{username} has been added to the list of admins", "Userlist")

def admin_del(username):
    admins.discard(username)
    save_admins(admins)
    log(f"{username} was removed from the list of admins", "Userlist")

def is_admins(username):
    if username == config["owner_user"]:
         return True
    else:
        return username in admins


        
#command

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


#message

def admins_handler(message, _):
    if message.chat.id == config["owner_id"]:
        add = user.get_state(message.chat.id, "admin_add_state", None)
        remove = user.get_state(message.chat.id, "admin_remove_state", None)
        
        if add:
            username = message.text
            admin_add(username)
            user.update_state(config["owner_id"], "admin_add_state", False)
            bot.send_message(config["owner_id"], f"Пользователь @{username} был дабавлен в список админов!")
            return True
        
        if remove:
            username = message.text
            admin_del(username)
            verify_state = user.update_state(config["owner_id"], "admin_remove_state", False)
            bot.send_message(config["owner_id"], f"Пользователь @{username} был удален из списка адмионов")
            return True



#inline

def admins(call, query):
    if query[0] == "add":
        atus_add_state = user.update_state(config["owner_id"], "admin_add_state", True)
        bot.send_message(config["owner_id"], "Введите никнейм пользователя, которого хотите добавить в спиок админов")
    if query[0] == "remove":
        atus_add_state = user.update_state(config["owner_id"], "admin_remove_state", True)
        bot.send_message(config["owner_id"], "Введите никнейм пользователя, которого хотите убрать из списка админов")