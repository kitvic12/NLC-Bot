from api import bot
import userstate
from config import config

def admins(call, query):
    if query[0] == "add":
        atus_add_state = userstate.update_state(config["owner_id"], "admin_add_state", True)
        bot.send_message(config["owner_id"], "Введите никнейм пользователя, которого хотите добавить в спиок админов")
    if query[0] == "remove":
        atus_add_state = userstate.update_state(config["owner_id"], "admin_remove_state", True)
        bot.send_message(config["owner_id"], "Введите никнейм пользователя, которого хотите убрать из списка админов")