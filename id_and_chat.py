from api import bot
import pickle
from telebot.types import Message
import os

file = "./chat_and_id"

dicts = None

def load():
    if dicts:
        return dicts
    try:
        with open(file, 'rb') as file:
            return dicts := dict(pickle.load(file))
    except FileNotFoundError:
        return dict()
    

def remove():
    os.remove(file)
    

def save(dicts):
    with open(file, 'wb') as file:
        pickle.dump(dict(dicts), file)


def new_id(message:Message, location):
    chat = message.chat.id
    id = message.id
    dicts = load()
    if location not in dicts: dicts[location] = dict()
    dicts[location][id] = chat
    save(dicts)


def check_mes(message:Message):
    dicts = load()
    chat = message.chat.id
    id = message.reply_to_message.id
    for elem in dicts:
        if id in dicts[elem]:
            loc = elem
            if dicts[elem][id] == chat:
                bot.delete_message(chat, id)
            else:
                bot.send_message(message.chat.id, "Ошибка в удалении сообщений в вашем чате")
            break
    
    for id in dicts[loc]:
        for chat in dicts[loc][id]:
            try:
                bot.delete_message(chat, id)
            except:
                bot.send_message(message.chat.id, "Ошибка в удаление сообщений в других чатах")