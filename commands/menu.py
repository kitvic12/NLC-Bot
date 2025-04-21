from api import bot
from log import log
from telebot import types

from inline import subscribe

from database import activity_tracker

@bot.message_handler(commands=["menu"])
def menu_cmd(message):
    log(f"{message.from_user.username} opened the menu", "Commands")
    activity_tracker.update_activity(message.from_user, 'command')
    menu(message)

def menu(message):
    check = subscribe.check_user(message.chat.id)

    if check:
        bot.send_message(message.chat.id, f"Вот что я могу:", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Посмотреть камеры", callback_data="see_video"),
        types.InlineKeyboardButton("Можно ли увидеть СО сейчас?", callback_data="see_now")],
        [types.InlineKeyboardButton("Выключить оповещения", callback_data="subscribe off"),
        types.InlineKeyboardButton("Сообщить о видимости", callback_data="will_see")],
        [types.InlineKeyboardButton("Узнать тип СО", callback_data="nlc check")]]
        ))
    else:
        bot.send_message(message.chat.id, f"Вот что я могу:", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Посмотреть камеры", callback_data="see_video"),
        types.InlineKeyboardButton("Можно ли увидеть СО сейчас?", callback_data="see_now")],
        [types.InlineKeyboardButton("Включить оповещения", callback_data="subscribe on"),
        types.InlineKeyboardButton("Сообщить о видимости", callback_data="will_see")],
        [types.InlineKeyboardButton("Узнать тип СО", callback_data="nlc check")]]
        ))