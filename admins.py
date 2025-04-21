from api import bot
from telebot import types
from config import config
import pickle
from log import log

FILE_PATH3 = "admin.pkl"

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