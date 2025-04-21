from api import bot
from admins import is_admins
from inline.subscribe import load_data
from telebot.types import Message
import pickle

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["fake"])
def fake(message:Message):
    if not message.reply_to_message:
        return
    notifications = pickle.load(open("./notifications.pkl", "rb"))
    id = False
    for i in notifications["data"]:
        s = notifications["data"][i]
        print(s)
        if (message.reply_to_message.chat.id, message.reply_to_message.message_id) in s:
            id = i
            mes = bot.send_message(message.chat.id, "Начинается удаление всех оповещений, ожидайте...")
            break
    else:
        bot.send_message(message.chat.id, "Упс, это не уведомление о СО")
        return
    
    for i in notifications["data"][id]:
        bot.delete_message(i[0], i[1])
    del notifications["data"][id]
    pickle.dump(notifications, open("./notifications.pkl", "wb"))
    bot.edit_message_text("Удаление успешно завершено! Спасибо за содействие!", message.chat.id, mes.id )
