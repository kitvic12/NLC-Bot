from api import bot
from log import clear_log
from admins import is_admins
from log import log
from user_activity import activity_tracker
from database import user

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["clear"])
def clear_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    what = message.text.split()
    log(f"{message.from_user.username} wants to clear {what[1]}", "Commands")
    if "log" in what[1]:
        result = clear_log(what[1], message.chat.id)
        if result:
            bot.send_message(message.chat.id, "Лог успешно очищен!")
            log(f"{what[1]} have been cleared", "Info")
    elif what[1] == "userstate":
        res = user.clear_all_userstates()
        bot.send_message(message.chat.id, f"Очистка выполнена успещно, затронуто {res} пользователей")