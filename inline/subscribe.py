from database import user

from log import log

from config import config
from api import bot

from telebot import types

from commands import menu

def need_resp(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)

    if query[0] == "off":
        user.set_notification(call.message.chat.id, "off")
        bot.send_message(call.message.chat.id, "Уведомления успешно отключены!")
        log(f"{user} notifications are turned off")

    elif query[0] == "on":
        user.set_notification(call.message.chat.id, "on")
        bot.send_message(call.message.chat.id, "Уведомления успешно включены!")
        log(f"{user} notifications enabled")

    menu.menu(call.message)