from api import bot
from database import user
from config import config
from telebot.types import Message

def resp_handler(message, _):
    state = user.get_state(message.chat.id, "callback", False)
    if state: 
        bot.forward_message(config["owner_id"], message.chat.id, message.id)
        bot.send_message(message.chat.id, "Благодарим за бдительность! Мы постараемся устранить неполадки как можно скорее, сразу после исправления ошибок, мы сообщим вам!")
        user.update_state(message.chat.id, "callback", False)
        user.update_state(config["owner_id"], "need_res", True)
        return True
    
def owner_respons(message:Message, _):
    if message.reply_to_message:
        bot.send_message(message.chat.id, "Ваше сообщение с ответом было успешно отправлено!")
        user.update_state(config["owner_id"], "need_res", False)
        bot.send_message(message.reply_to_message.forward_from.id, f"Получен ответ на ваше обращение в тех поддержку: {message.text}")
        return True