from api import bot
from log import log
from telebot import types
from admins import is_admins

from user_activity import activity_tracker

@bot.message_handler(commands=["help"])
def help_cmd(message):
  log(f"{message.from_user.username} wrote help")
  activity_tracker.update_activity(message.from_user, 'command')
  bot.send_message(message.chat.id, "Я могу показать камеры, включить опопвещения о появлениях СО в нужном регионе, рассказать вероятоть появления СО сейчас, помочь с типом СО и рассказать что такое СО. Для рассказа о том, что такое СО напишите /about, для вызова функция связаных с СО сейчас напишите /menu, в случае ошибки используйте обратную связь с помощью команды  /callback")

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["helpa"])
def admin_command(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log(f"{message.from_user.username} wrote admin_help", "Commands")
    bot.send_message(message.chat.id, f"/fake - !указывать только ответом на сообщение! опровергает найденые ботом серебристые облака \n /get  - запросить логи (log, errorlog, checklog) \n /users - показывает всех пользователей и всю их статистику \n /clear - очищает логи(log, errorlog, checklog) \n /allusers - показывает полную базу данных по пользователям")