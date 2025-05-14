from api import bot
from database import db_for_send
from user_activity import activity_tracker
from admins import is_admins
from log import log

@bot.message_handler(func=lambda message:is_admins(message.from_user.username), commands=["allusers"])
def send_db(message):
    activity_tracker.update_activity(message.from_user, 'command')  
    log(f"{message.from_user.username} required database of all user", "Commands")
    db_parts = db_for_send()
    for part in db_parts:
        bot.send_message(message.chat.id, f"<pre>{part}</pre>", parse_mode='HTML')
