from api import bot
from log import log

from user_activity import activity_tracker

@bot.message_handler(commands=["start"])
def start_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_message(message.chat.id, f"Здравствуйте @{message.from_user.username}! Мы рады приветствовать вас в боте, который помогает в отслежевании появлений серебристых облаков! Для более подробной информации о способностях нашего бота напишите /help. У нас есть [свой канал](https://t.me/kitvic_nlc_chanel), там вы можете узнавать актуальную информацию о всех изменениях бота и задавать впорпосы на прямую в комментариях!", parse_mode='Markdown')
    log(f"{message.from_user.username} wrote start")