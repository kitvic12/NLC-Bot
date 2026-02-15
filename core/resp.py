from .api import bot
def resp_all(message, wastriggered):
    if not wastriggered:
        if "/" in message.text:
            bot.send_message(message.chat.id, "Извините, данной команды не существует или у вас нет прав на ее использование.")
            return
        bot.send_message(message.chat.id, "Извините, ваш запрос не известен, для того чтобы узнать возможности бота используйте /help.")