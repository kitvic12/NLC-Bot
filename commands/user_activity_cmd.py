import time

from log import log

from config import config

from user_activity import activity_tracker, MOSCOW_TZ

from api import bot

from admins import is_admins

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=['users'])
def show_all_users(message):

    activity_tracker.update_activity(message.from_user, 'command')
    users = activity_tracker.get_all_users()
    log("The owner requested the database", "Commands")

    if not users:
        bot.reply_to(message, "В базе нет пользователей")
        return
    
    response = "📊 Все пользователи:\n\n"
    count = 0
    for user_id, data in users.items():
        count += 1
        moscow_time = data['last_seen'].astimezone(MOSCOW_TZ)  
        next_user = (
            f"👤 {data['first_name']} {data.get('last_name', '')}\n"
            f"🆔 ID: {user_id} | @{data.get('username', 'нет')}\n"
            f"📅 Первый вход: {data['first_seen'].astimezone(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"⏱ Последняя активность: {moscow_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"✉️ Сообщения: {data['actions']['messages']} | "
            f"⌨️ Команды: {data['actions']['commands']} | "
            f"🔘 Inline: {data['actions']['inline']}\n"
            f"--------------------------------\n"
        )
        if len(response) + len(next_user) >= 4000:
            bot.reply_to(message, response)
            response = next_user
            time.sleep(1)
            continue
        else:
            response += next_user

    bot.send_message(message.chat.id, f"Всего пользователей: {count}")