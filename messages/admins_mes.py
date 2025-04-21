import userstate 
from api import bot
from config import config

from admins import admin_add, admin_del

def admins_handler(message, _):
    if message.chat.id == config["owner_id"]:
        add = userstate.get_state(message.chat.id, "admin_add_state", None)
        remove = userstate.get_state(message.chat.id, "admin_remove_state", None)
        
        if add:
            username = message.text
            admin_add(username)
            userstate.update_state(config["owner_id"], "admin_add_state", False)
            bot.send_message(config["owner_id"], f"Пользователь @{username} был дабавлен в список админов!")
            return True
        
        if remove:
            username = message.text
            admin_del(username)
            verify_state = userstate.update_state(config["owner_id"], "admin_remove_state", False)
            bot.send_message(config["owner_id"], f"Пользователь @{username} был удален из списка адмионов")
            return True