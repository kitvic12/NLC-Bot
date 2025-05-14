from api import bot
from log import clear_log
from admins import is_admins
from log import log
from user_activity import activity_tracker

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["clear"])
def clear_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    logs = message.text.split()
    log(f"{message.from_user.username} wants to clear {logs[1]}", "Commands")
    result = clear_log(logs[1], message.chat.id)
    if result:
        bot.send_message(message.chat.id, "Лог успешно очищен!")
        log(f"{logs[1]} have been cleared", "Info")
        