import requests
from bs4 import BeautifulSoup

from core.api import bot


city_map = {
    "Азево": "https://starvisor.ru/azv/", 
    "Айхал": "https://starvisor.ru/ayk/",
    "Альметьевск": "https://starvisor.ru/almet/",
    "Васкелово": "https://starvisor.ru/spbd/",
    "Багдарин": "https://starvisor.ru/bag/",
    "Березники": "https://starvisor.ru/brz/",
    "Вологда": "https://starvisor.ru/vlg/",
    "Гулькевичи": "https://starvisor.ru/gul/",
    "Воркута": "https://starvisor.ru/vrk/",
    "Провидения": "https://starvisor.ru/prv/",
    "Ирбит": "https://starvisor.ru/irb/",
    "Калининград": "https://starvisor.ru/kln/",
    "Калуга": "https://starvisor.ru/klg/",
    "Каменск-Уральский": "https://starvisor.ru/kur/", 
    "Краснодар": "https://starvisor.ru/nov/",
    "Москва": "https://starvisor.ru/msc/",
    "Остроленский": "https://starvisor.ru/ost/",
    "Пермь": "https://starvisor.ru/prm/",
    "Попово": "https://starvisor.ru/ppv/",
    "Пятиречье": "https://starvisor.ru/ptr/",
    "Русское": "https://starvisor.ru/rus/",
    "Рязань": "https://starvisor.ru/rzn/",
    "Стрежевой": "https://starvisor.ru/str/",
    "Тула": "https://starvisor.ru/tula/",
    "Уткино": "https://starvisor.ru/utk/",
    "Челябинск": "https://starvisor.ru/chb/",
    "Юрга": "https://starvisor.ru/yur/",
    "Ярославль": "https://starvisor.ru/yar/", 
    "Тырнауз": "https://gw.cmo.sai.msu.ru/webcam6.jpg"
}

def get_camera_image(city):
    URL = city_map[city]
    response = requests.get(URL)
    if city == "Тырнауз":
        if response.status_code == 200:
            return response.content
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        camera_image = soup.find('img', class_='single-city-image')  
        if camera_image:
            image_url = camera_image['src']
            if not image_url.startswith('http'):
                image_url = URL + image_url
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                return image_response.content
    return None

def send_image_to_telegram(image_bytes, id):
    try:
        bot.send_photo(id, photo=image_bytes)
    except:
        print("Ошибка отправки")