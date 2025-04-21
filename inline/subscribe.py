import pickle

from log import log

from config import config
from api import bot

from telebot import types

from commands import menu

FILE_NAME = "places_users.pkl"


def save_data(data):
    with open(FILE_NAME, "wb") as file:
        pickle.dump(data, file)


def load_data():
    try:
        with open(FILE_NAME, "rb") as file:
            data = pickle.load(file)
            if not isinstance(data, set):  
                return set()
            return data
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return set()  

places_users = load_data()


def add_user(user):
    users = load_data()  
    users.add(user)
    save_data(users)  
    log(f"{user} notifications enabled")

def remove_user(user):
    users = load_data()  
    users.discard(user)
    save_data(users)  
    log(f"{user} notifications are turned off")

def check_user(user):
    users = load_data() 
    return user in users

def need_resp(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)

    if query[0] == "off":
        remove_user(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Уведомления успешно отключены!")
    elif query[0] == "on":
        add_user(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Уведомления успешно включены!")

    menu.menu_cmd(call.message)