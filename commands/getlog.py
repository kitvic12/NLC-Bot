from api import bot
from telebot import types
from config import config
from log import log_file, log, error_log_file
from config import config
from admins import is_admins

from user_activity import activity_tracker

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["get"])
def get(message):
    if "checklog" in message.text:
        getchecklog_command(message)
        return
    elif "errorlog" in message.text:
        geterrorlog_command(message)
        return
    elif "log" in message.text:
        getlog_command(message)
        return

def getlog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a log", "Command")
    file = open(r"./botlog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")


def geterrorlog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a errorlog", "Command")
    file = open(r"./errorlog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")


def getchecklog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a checklog", "Command")
    file = open(r"./checklog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")