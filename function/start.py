from core.api import bot
from core.log import log

from core.user_activity import activity_tracker

@bot.message_handler(commands=["start"])
def start_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    text = f"""Здравствуйте, @{message.from_user.username}! Мы рады приветствовать вас в боте, который помогает в отслеживании появлений серебристых облаков! Для более подробной информации о способностях нашего бота напишите /help. У нас есть <a href="https://t.me/kitvic_nlc_chanel">свой канал</a>, там вы можете узнавать актуальную информацию о всех изменениях бота и задавать вопросы напрямую в комментариях!"""
    bot.send_message(message.chat.id, text, parse_mode='HTML')
    log(f"{message.from_user.username} wrote start")