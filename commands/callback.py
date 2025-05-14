from api import bot
from config import config

from log import log
from telebot import types

from user_activity import activity_tracker

from database import user

@bot.message_handler(commands=['callback'])
def callback_handler(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log(f"{message.from_user.username} requests technical support", "Commands")
    user.update_state(message.chat.id, "callback", True) 
    bot.send_message(message.chat.id, "Напишите пожалуйста ваши претензии или замечания в работе бота, сразу же после их исправления или просто ответа от тех. поддержки, мы сразу же сообщим вам об этом. Спасибо за внимательность!", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Отмена", callback_data=f"menu yes callback")]]
    ))