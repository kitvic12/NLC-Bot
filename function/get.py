from core.api import bot
from telebot import types
from core.config import config
from core.log import log_file, log, error_log_file
from core.config import config
from .admins import is_admins
from core.database import db_for_send
from core.user_activity import activity_tracker
from .admins import is_admins
from core.log import log
import time
from core.user_activity import activity_tracker




@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["get"])
def get(message):
    what = message.text.split()
    if what[1] == "checklog":
        getchecklog_command(message)
        return True
    elif what[1] == "errorlog":
        geterrorlog_command(message)
        return True
    elif what[1] == "log":
        getlog_command(message)
        return True
    elif what[1] == "config":
        send_db(message)
        return True

def getlog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a log", "Command")
    file = open(r"./files/botlog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")


def geterrorlog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a errorlog", "Command")
    file = open(r"./files/errorlog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")


def getchecklog_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log("Owner required a checklog", "Command")
    file = open(r"./files/checklog.log", "rb")
    bot.send_document(chat_id=message.chat.id, document=file, caption="Вот ваш лог")

def send_db(message):
    activity_tracker.update_activity(message.from_user, 'command')  
    log(f"{message.from_user.username} required database of all user", "Commands")
    db_parts = db_for_send()
    for part in db_parts:
        bot.send_message(message.chat.id, f"<pre>{part}</pre>", parse_mode='HTML')
        time.sleep(1)