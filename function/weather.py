import requests
from core.log import check

locations = {
    "Азево": {"lat": 56, "lon": 53},
    "Айхал": {"lat": 65, "lon": 111},
    "Альметьевск": {"lat": 54, "lon": 52},
    "Багдарин": {"lat": 54, "lon": 113},
    "Березники": {"lat": 59, "lon": 57},
    "Васкелово": {"lat": 60, "lon": 30},
    "Вологда": {"lat": 59, "lon": 39},
    "Воркута": {"lat": 67, "lon": 64},
    "Гулькевичи": {"lat": 45, "lon": 40},
    "Ирбит": {"lat": 57, "lon": 63},
    "Калининград": {"lat": 54, "lon": 20},
    "Калуга": {"lat": 54, "lon": 36},
    "Каменск-Уральский": {"lat": 56, "lon": 61},
    "Краснодар": {"lat": 45, "lon": 38},
    "Москва": {"lat": 55, "lon": 37},
    "Остроленский": {"lat": 53, "lon": 59},
    "Пермь": {"lat": 58, "lon": 56},
    "Попово": {"lat": 57, "lon": 38},
    "Провидения": {"lat": 64, "lon": -173},
    "Пятиречье": {"lat": 60, "lon": 30},
    "Русское": {"lat": 47, "lon": 38},
    "Рязань": {"lat": 54, "lon": 40},
    "Стрежевой": {"lat": 61, "lon": 77},
    "Тула": {"lat": 54, "lon": 37},
    "Уткино": {"lat": 57, "lon": 40},
    "Челябинск": {"lat": 55, "lon": 61},
    "Юрга": {"lat": 55, "lon": 84},
    "Ярославль": {"lat": 57, "lon": 39},
    "Тырнауз": {"lat": 42, "lon":43}
}


API_KEY = 'f0edf143fa18b97714580792348b7c52'


def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def check_cloudiness(lat, lon, location):
    weather_data = get_weather(lat, lon)
    if weather_data:
        current_weather = weather_data["current_weather"]
        temperature = current_weather["temperature"]
        wind_speed = current_weather["windspeed"]
        weather_code = current_weather["weathercode"]

        
        weather_codes = {
            0: True,
            1: True,
            2: False,
            3: False,
            45: False,
            48: False,
            51: False,
            53: False,
            55: False,
            56: False,
            57: False,
            61: False,
            63: False,
            65: False,
            71: False,
            73: False,
            75: False,
            77: False,
            80: False,
            81: False,
            82: False,
            85: False,
            86: False,
            95: False,
            96: False,
            99: False
        }
        weather_description = weather_codes.get(weather_code, "Неизвестно")
        check(f"{location}: {weather_description}", "WEATHER")
        return weather_description



