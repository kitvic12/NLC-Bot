from AI.types.check_nlc import handle_photo
from database import user
from api import bot

def handle_nlc_photo(message, _):
    state = user.get_state(message.chat.id, "types nlc")
    id = user.get_state(message.chat.id, "id")
    if state:
        bot.delete_message(message.chat.id, id)
        handle_photo(message)