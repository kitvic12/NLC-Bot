from api import bot
from log import log
from telebot import types
from admins import is_admins

from user_activity import activity_tracker

command = {
   "fake": "Указывать только ответом на сообщение о наличие СО, она будет удалять данное оповещение, если вы как админ, считаете. что оно ложное",
   "get": "Данная команда позволяет получить файлы с информацией о пользователях и действиях бота \n -log - обычные логи бота \n -errorlog - логи ошибок бота \n -checklog - логи выполнения проверок на наличие СО и просто облачности \n -config - JSON файл со всеми userstate и пользователями бота",
   "clear": "Очищает данные разных файлов с данными о работе бота и действиями пользователей \n -log - обычные логи бота \n -errorlog - логи ошибок бота \n -checklog - логи выполнения проверок на наличие СО и просто облачности \n -userstate - уникальное значение действия для каждого пользователя",
   "users": "Выводит список, количество и статистику всех пользователей бота"
}

@bot.message_handler(commands=["help"])
def help_cmd(message):
  log(f"{message.from_user.username} wrote help")
  activity_tracker.update_activity(message.from_user, 'command')
  bot.send_message(message.chat.id, "Я могу показать камеры, включить оповещения о появлениях СО в нужном регионе, рассказать вероятность появления СО сейчас, помочь с типом СО и рассказать, что такое СО. Для рассказа о том, что такое СО напишите /about, для вызова функция связанных с СО сейчас напишите /menu, в случае ошибки используйте обратную связь с помощью команды  /callback")

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["helpa"])
def admin_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log(f"{message.from_user.username} wrote admin_help", "Commands")
    bot.send_message(message.chat.id, f"/fake - !указывать только ответом на сообщение! опровергает найденые ботом серебристые облака \n /get  - запросить логи (log, errorlog, checklog, config) \n /users - показывает всех пользователей и всю их статистику \n /clear - очищает логи(log, errorlog, checklog, userstate) \n /what - позволяет узнать о любой команде админа более подробно")

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["what"])
def what_cmd(message):
   what = message.text.split()[1]
   bot.send_message(message.chat.id, f"Команда /{what}: \n" + command[what])