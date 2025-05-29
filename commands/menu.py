from api import bot
from log import log
from telebot import types

from database import user

from user_activity import activity_tracker

@bot.message_handler(commands=["menu"])
def menu_cmd(message):
    user.clear_user_markup(message.chat.id)
    log(f"{message.from_user.username} opened the menu", "Commands")
    activity_tracker.update_activity(message.from_user, 'command')
    menu_send(message)

def checker(id): 
    check = user.check(id)
    murkup = types.InlineKeyboardMarkup()
    murkup.add(types.InlineKeyboardButton("Посмотреть камеры", callback_data="see_video"), 
                types.InlineKeyboardButton("Можно ли увидеть СО сейчас?", callback_data="see_now"))
    if check:
        murkup.add(types.InlineKeyboardButton("Выключить оповещения", callback_data="subscribe off"),
        types.InlineKeyboardButton("Сообщить о видимости", callback_data="will_see"))
    else:
        murkup.add(types.InlineKeyboardButton("Включить оповещения", callback_data="subscribe on"),
        types.InlineKeyboardButton("Сообщить о видимости", callback_data="will_see"))   
    murkup.add(types.InlineKeyboardButton("Анализ фото", callback_data="nlc check"))   
    return murkup


def menu_send(message):
    markup = checker(message.chat.id)
    bot.send_message(message.chat.id, "Вот что я могу:", reply_markup=markup)
   
def menu(message, where="no"): 
    if where == "yes": 
        murkup = checker(message.chat.id)
        bot.edit_message_text("Вот что я могу:", message.chat.id, message.id)
        bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=murkup)
    elif where == "no": 
        menu_send(message)

