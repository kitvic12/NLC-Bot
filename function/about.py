from core.api import bot
from telebot import types
from core.main import change_for_about
from telebot.types import InputMediaPhoto
from core.user_activity import activity_tracker



#command

@bot.message_handler(commands=["about"])
def about_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_message(
    message.chat.id,  
    "В данной команде вы можете узнать как и о самих серебристых облаках(СО), так и о параметрах которые рекомендуется записывать во время набюдений для сбора статистики (также их можно отправлять в наш бот /menu -> 'Поделиться наблюдением').",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Параметры видимости СО", callback_data=f"nlc choise_par {True}")],
         [types.InlineKeyboardButton("Базовые понятия о СО", callback_data=f"nlc about {True}")]]
    ))


#inline

def load_image(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


main_data = {
    "main True":{"text":"В данной команде вы можете узнать как и о самих серебристых облаках(СО), так и о параметрах которые рекомендуется записывать во время набюдений для сбора статистики (также их можно отправлять в наш бот /menu -> 'Поделиться наблюдением').", "photo":False, "murkup":[f"choise_par {True}", f"about {True}"], "text_murkup":["Параметры видимости СО", "Базовые понятия о СО"]},
    f"choise_par True":{"text":"Запись параметров серебристых облаков при наблюдениях важна для изучения физических процессов в верхних слоях атмосферы, в частности, в мезосфере. Эти облака являются чувствительным индикатором изменений климата и антропогенного воздействия, таких как увеличение содержания метана. Систематические наблюдения позволяют отслеживать динамику стратосферы и мезосферы, а также изучать процессы формирования и распространения серебристых облаков", "photo":False, "murkup":[f"light {True}", f"intensity {False}", f"area {False}", f"weather {True}", "main True"], "text_murkup":["Яркость", "Интенсивность", "Площадь", "Погода", "Назад"]},
    f"about True":{"text":"Серебристые облака - это сравнительно редкое атмосферное явление, крайне разрежённые облака, состоящие из мелких льдинок, которые подсвечивает солнце. Возникают эти облака в мезосфере под мезопаузой (на высоте 76—85 км над поверхностью Земли) и видимые в глубоких сумерках, непосредственно после заката или перед восходом Солнца. \n Также у серебристых облаков есть свои типы, о них вы можете узнать нажав на кнопку ниже", "photo":r"function/photo/NLC.jpg", "murkup":[f"type {True}", "main True"], "text_murkup":["Типы СО", "Назад"]},

    f"light True":{"text":"Яркость серебристых облаков - один из важнейших параметров который нужно записывать при наблюдениях. Вы можете выбрать о какой конкретном показателе яркости вы хотите посмотреть.", "photo":r"function/photo/light.png", "murkup":["light 1", "light 2", "light 3", "light 4", "light 5", "choise_par True"], "text_murkup":["1", "2", "3", "4", "5", "Назад"]},
    "light 1":{"text":"Индекс яркости 1 \n Очень слабые серебристые облака, едва видимые на фоне сумеречного неба; определимы только при очень тщательном изучении неба.", "photo":r"function/photo/light_1.png", "murkup":[f"light {True}"]},
    "light 2":{"text":"Индекс яркости 2 \n Серебристые облака легко определимы, но имеют низкую яркость.", "photo":r"function/photo/light_2.png", "murkup":[f"light {True}"]},
    "light 3":{"text":"Индекс яркости 3 \n Серебристые облака хорошо видны, четко выделяясь на фоне сумеречного неба.", "photo":r"function/photo/light_3.png", "murkup":[f"light {True}"]},
    "light 4":{"text":"Индекс яркости 4 \n Серебристые облака очень яркие и привлекают внимание наблюдателей-неспециалистов.", "photo":r"function/photo/light_4.png", "murkup":[f"light {True}"]},
    "light 5":{"text":"Индекс яркости 5 \n Серебристые облака крайне яркие и заметно освещают повернутые к ним предметы.", "photo":r"function/photo/light_5.png", "murkup":[f"light {True}"]},

    f"type True":{"text":"Выберите тип, о котором хотите узнать", "photo":False, "murkup":["type fler", "type str", "type waves", "type winds", "about True"], "text_murkup":["Флер", "Полосы", "Волны", "Вихри", "Назад"]},
    "type fler": {"text":"Тип 1, Флер \n Cтруктура, не имеющая определенных очертаний, которые иногда отражают фоном другие облачные формы. Флер похож на однородную или неоднородную пелену. Довольно часто, спустя примерно полчаса после появления флера, наблюдаются серебристые облака с более развитой структурой. Далее флер сочетается с другими формами.", "photo":r"function/photo/fler.png", "murkup":["type True"]},
    "type str":  {"text":"Тип 2, Полосы \n Тип 2А - размытые полосы \n Состоят из линий с нечеткими краями. \n Тип 2Б -  резко-очерченные \n Состоят из линий с хорошо определенными краями. Полосы могут менять яркость всей структуры в течение 20-60 минут.", "photo":r"function/photo/str.png", "murkup":["type True"]},
    "type waves":{"text":"Тип 3, Волны \n Гребешки (III-a) \n участки с частым расположением узких, резко очерченных параллельных полос, наподобие легкой ряби на поверхности воды при небольшом порыве ветра.\n Гребни (III-b) \n имеют более заметные признаки волновой природы; расстояние между соседними гребнями в 10–20 раз больше, чем у гребешков. Волнообразные изгибы (III-c) образуются в результате искривления поверхности облаков, занятой другими формами (полосами, гребешками)", "photo":r"function/photo/waves.png", "murkup":["type True"]},
    "type winds":{"text":"Тип 4, Вихри \n Частичные или, в редких случаях, полные кольца облаков с темной серединой. Иногда можно наблюдать во флёре, полосах и волнах. Выделяют три группы: \n 4a) \n Завихрения и круглые просветы радиусом 0.1° — 0.5°. Завихрениям подвергаются полосы, гребешки и иногда флер. \n 4b) \n Завихрение в виде простого изгиба одной или нескольких полос в сторону от основного направления с радиусом 3°–5°. Часто образуются в облаках, имеющих полосчатое и струйчатое строение. \n 4c) \n Мощные вихревые выбросы в сторону от основного облака", "photo":r"function/photo/winds.png", "murkup":["type True"]},

    f"area False":{"text":"Руководство по определению площади СО на небе \n Выбирается столбец отношения СО к площади неба(A), и строка яркости(B).На их пересечении находится балл интенсивности в вашем случае. На этом снимке представлены серебристые облака. Можно заметить, что они занимают около ¾ области сумеречного участка неба. С помощью шкалы яркости можно определить, что яркость этих облаков примерно 4 балла. Следственно, мы ищем пересечение этих параметров в таблице и получаем, что интенсивность данных серебристых облаков равна 7 баллам.", "photo":r"function/photo/area.png", "murkup":["choise_par True"]},

    f"intensity False":{"text":"Интенсивность серебристых облаков \n Она определяется по 10-балльной шкале на основе: \n A – отношение площади СО к сумеречному сегменту неба. \n B – яркость СО по 5-балльной шкале. \n Дополнительные параметры:\n   S или D – видны только фрагменты СО. \n  M – наблюдается многослойность. \n", "photo":r"function/photo/intensity.png", "murkup":["choise_par True"]},

    f"weather True":{"text":"Погодные условия \n В случае с наблюдениями серебристых облаков, погодные условия мы записываем чтобы ", "photo":False, "murkup":['weather 1', "weather 2", "weather 3", "weather 4", "weather 5", "choise_par True"], "text_murkup":["А", "Б", "В", "Г", "Д", "Назад"],},
    "weather 1":{"text":"А – облаков в зоне сумеречного сегмента нет или их наличие не мешает наблюдениям. Облачность до 20%.", "photo":r"function/photo/weather_1.png", "murkup":["weather True"]},
    "weather 2":{"text":"Б - сумеречная часть неба незначительно покрыта облачностью (сегмент закрыт от 20 до 50%.)", "photo":r"function/photo/weather_2.png", "murkup":["weather True"]},
    "weather 3":{"text":"В - сумеречная часть неба значительно покрыта облачностью (сумеречный сегмент закрыт на 50–80%)", "photo":r"function/photo/weather_3.png", "murkup":["weather True"]},
    "weather 4":{"text":"Г – Сумеречная часть неба почти полностью покрыта облачностью (>80%), наблюдаются лишь редкие просветы (сегмент закрыт от 80 до 95%)", "photo":r"function/function/photo/weather_4.png", "murkup":["weather True"]},
    "weather 5":{"text":"Д – Сумеречная часть неба полностью закрыта облачность (сумеречный сегмент закрыт на 95–100% облачностью.)", "photo":r"function/function/photo/weather_5.png", "murkup":["weather True"]}
}


def main_handler(call, query):
    what = main_data[" ".join(query[0::])]
    murkup = types.InlineKeyboardMarkup()
    if query[1]:
        if query[1] == "True":
            for i in range(len(what["murkup"])):
                murkup.add(types.InlineKeyboardButton(text=what["text_murkup"][i], callback_data=f"nlc {what['murkup'][i]}"))
        else:
            murkup.add(types.InlineKeyboardButton(text="Назад", callback_data=f"nlc {what['murkup'][0]}"))
    else: 
        murkup.add(types.InlineKeyboardButton(text="Назад", callback_data=f"nlc {what['murkup'][0]}"))


    text = what["text"]
    if what["photo"]:
        photo = load_image(what["photo"])
    else:
        photo = None

    change_for_about(message=call.message, text=text, media=photo, markup=murkup)