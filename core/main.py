from .api import bot
from function.menu import menu
from .database import user
from telebot import types

def change(message, text=None, reply_markup=None, media=None): 
    if media is not None:
        bot.edit_message_media(media=media, chat_id=message.chat.id, reply_markup=reply_markup)

    if text and reply_markup: 
        bot.edit_message_text(text, message.chat.id, message.id, reply_markup=reply_markup)
    if reply_markup and not text:
        bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup)
    if text and not reply_markup:
        bot.edit_message_text(text, message.chat.id, message.id)



def return_menu(call, query):
    try:
        if query[0] == "yes": 
            if query[1] == "callback":
                user.update_state(call.message.chat.id, "callback", False)
            elif query[1] == "nlc_types":
                user.update_state(call.message.chat.id, "types nlc", False)
            elif query[1] == "see_now":
                user.update_state(call.message.chat.id, "see_now", False)

        menu(call.message, query[0]) 
        return   

    except:
        user.clear_user_markup(call.message.chat.id)
        menu(call.message, "no")
        bot.delete_message(call.message.chat.id, call.message.id)


def change_for_about(message, markup, media=None, text=None):
    try:
        if media:
            if message.content_type == 'photo':
                try:
                    bot.edit_message_media(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        media=types.InputMediaPhoto(media, caption=text),
                        reply_markup=markup
                    )
                    return 
                except Exception as e:
                    print(f"Не удалось изменить медиа: {e}")
        else:
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=text,
                    reply_markup=markup
                )
                return 
            except Exception as e:
                print(f"Не удалось изменить текст: {e}")

        try:
            bot.delete_message(message.chat.id, message.id)
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        if media:
            bot.send_photo(message.chat.id, media, caption=text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text, reply_markup=markup)

    except Exception as e:
        print(f"Ошибка в change_for_about: {e}")
        if media:
            bot.send_photo(message.chat.id, media, caption=text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text, reply_markup=markup)