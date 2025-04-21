from api import bot
from config import config


from message import callback_message, callback_image
from inlines import callback_inline


import log
import traceback
import time

import pytz
from datetime import datetime

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

def moscow_time():
    now = datetime.now(MOSCOW_TZ)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def start_bot():
    count = 0
    last_error = ' '
    while True:
        try:
            times = moscow_time()
            bot.send_message(config["owner_id"], "Бот сартует")
            log.log_init()
            log.log(f"Start at {times}") 
            log.error_init()
            log.error(f"Start at {times}") 
            bot.polling()
            count = 0
            last_error = " "
        except Exception as e:
            error_message = f"Ошибка: {str(e)}\n\nТрассировка:\n{traceback.format_exc()}"
            log.error(error_message, "ERROR")
            if count != 1 and error_message == last_error:
                pass
            else:
                try:
                    bot.send_message(config["owner_id"], f"⚠️ Произошла ошибка:\n```\n{error_message}\n```", parse_mode="MarkdownV2")
                except Exception as send_error:
                    log.error(send_error, "SEND_ERROR")       
            last_error = error_message
            count += 1
            if count >= 15:
                try:
                    bot.send_message(config["owner_id"], f"🚨 Бот остановлен после 15 ошибок подряд.")
                except Exception as send_error:
                    log.error(f"Не удалось отправить сообщение об остановке: {send_error}", "SEND_ERROR")
                break
            time.sleep(10)




if __name__ == "__main__":
    start_bot()