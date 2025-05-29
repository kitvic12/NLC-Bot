from api import bot
from commands.menu import menu
from database import user

def change(message, text=None, reply_markup=None): 
    if text and reply_markup: 
        bot.edit_message_text(text, message.chat.id, message.id, reply_markup=reply_markup)
    elif reply_markup and not text:
        bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup)
    elif text and not reply_markup:
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