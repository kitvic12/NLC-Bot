from core.api import bot
from core.config import config
from core.log import log
from core.user_activity import activity_tracker
from core.database import user

from telebot import types


#command

@bot.message_handler(commands=['callback'])
def callback_handler(message):
    activity_tracker.update_activity(message.from_user, 'command')
    log(f"{message.from_user.username} requests technical support", "Commands")
    user.update_state(message.chat.id, "callback", True) 
    bot.send_message(message.chat.id, "Напишите пожалуйста ваши претензии или замечания в работе бота, сразу же после их исправления или просто ответа от тех. поддержки, мы сразу же сообщим вам об этом. Спасибо за внимательность!", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Отмена", callback_data=f"menu yes callback")]]
    ))



#message

def resp_handler(message, _):
    state = user.get_state(message.chat.id, "callback", False)
    if state: 
        bot.forward_message(config["owner_id"], message.chat.id, message.id)
        bot.send_message(message.chat.id, "Благодарим за бдительность! Мы постараемся устранить неполадки как можно скорее, сразу после исправления ошибок, мы сообщим вам!")
        user.update_state(message.chat.id, "callback", False)
        user.update_state(config["owner_id"], "need_res", True)
        return True
    
def owner_respons(message, _):
    if message.reply_to_message and message.chat.id == config["owner_id"] and user.get_state(config['owner_id'], "need res"):
        bot.send_message(message.chat.id, "Ваше сообщение с ответом было успешно отправлено!")
        user.update_state(config["owner_id"], "need_res", False)
        bot.send_message(message.reply_to_message.forward_from.id, f"Получен ответ на ваше обращение в тех поддержку: {message.text}")
        return True