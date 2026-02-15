from core.api import bot
from telebot import types
from core.database import user
from core.main import change



#inline

def see_nlc(call, query):
    change(call.message, 'Пожалуйста сообщите место, где вы их видите(не на небе, а где вы находитесь) или фото с подписью в виде указания места',
           reply_markup=types.InlineKeyboardMarkup(
               [[types.InlineKeyboardButton("Отмена", callback_data='menu yes see_now')]]
           ))
    user.update_state(call.message.chat.id, "see nlc", True)



#message

def send_all(message):
    if not message.photo:
        id = message.chat.id
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    bot.send_message(users['user_id'], f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        return
    
    if message.photo:
        id = message.chat.id
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    photo = message.photo[0]  
                    bot.send_photo(users['user_id'], photo.file_id, caption=f"Есть сообщения о видимости серебристых облаков в {message.caption}! Удачных вам наблюдений!")
        return



def place(message, _):
    if user.get_state(message.chat.id, "see nlc"):
        bot.send_message(message.chat.id, "Спасибо за информацию, мы воспользуемся ей и оповестим остальных пользователей!", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("В меню", callback_data="menu")]]
        ))
        user.update_state(message.chat.id, "see nlc", False)
        return True
    

def place_photo(message, _):
    if user.get_state(message.chat.id, "see nlc"):
        if message.from_user.is_bot: 
            return
        if not message.caption:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте заново ваше фото, где в подписи укажите место наблюдений!")
            user.update_state(message.chat.id, "see nlc", False)
            return
        if message.caption: 
            bot.send_message(message.chat.id, "Спасибо за информацию! Мы оповестим ей других пользователей.")
            send_all(message)
            return
        return True