from api import bot
import log
from AI.nlc_or_cloud.check_on_camera import handle_photo
from inline.subscribe import load_data
from camera.weather import check_cloudiness, locations
from camera.get_image import get_camera_image
import pytz
from datetime import datetime
import pickle
import os
from config import config

my_set = {config["owner_id"], config["psinka_id"], config["fish_id"]}

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

notifications = {
    "cid":0,
    "data":dict()
}
nfname = "./notifications.pkl"

def notifications_load():
    global notifications, nfname
    try:
        with open(nfname, "rb") as file:
            notifications = pickle.load(file)
    except FileNotFoundError:
        notifications_save()
    
def notifications_save():
    global notifications, nfname
    with open(nfname, "wb") as file:
        pickle.dump(notifications, file)

def moscow_time():
    now = datetime.now(MOSCOW_TZ)
    return now.strftime("%Y-%m-%d %H:%M:%S")

notifications_load()

def main_handler():
    for location in locations:
        lat = locations[location]["lat"]
        lon = locations[location]["lon"]
        cloud = check_cloudiness(lat, lon, location)
        if cloud:
            photo = get_camera_image(location)
            nlc = handle_photo(photo)
            if nlc:
                log.check(f"{location} may see nlc", "ALWAYS_CHECK")
                notifications_load()
                notifications["data"][notifications["cid"]] = set()
                for chat in my_set:
                    mes = bot.send_photo(chat, photo, f"Есть подозрение на наличие серебристых облаков на камере {location}!")
                    notifications["data"][notifications["cid"]].add((mes.chat.id, mes.message_id))
                notifications["cid"] += 1
                notifications_save()

if __name__ == "__main__":
    while True:
        log.check("----------------", "ALWAYS_CHECK")
        time = moscow_time()
        log.check(f"Start check at {time}", "ALWAYS_CHECK")
        main_handler()
        log.check("----------------", "ALWAYS_CHECK")
        import time
        time.sleep(3600)