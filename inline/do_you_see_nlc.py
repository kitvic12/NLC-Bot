from api import bot
from telebot import types
import userstate

def see_nlc(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, "Пожалуйста сообщите место, где вы их видите(не на небе, а где вы находитесь)")
    userstate.update_state(call.message.chat.id, "see nlc", True)