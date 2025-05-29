from api import bot
from telebot import types
from database import user
from main import change

def see_nlc(call, query):
    change(call.message, 'Пожалуйста сообщите место, где вы их видите(не на небе, а где вы находитесь) или фото с подписью в виде указания места',
           reply_markup=types.InlineKeyboardMarkup(
               [[types.InlineKeyboardButton("Отмена", callback_data='menu yes see_now')]]
           ))
    user.update_state(call.message.chat.id, "see nlc", True)