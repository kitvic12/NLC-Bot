from api import bot
from telebot import types


def load_image(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

try:
    light_data = load_image(r"photo/light.png")
    fler_data = load_image(r"photo/fler.png")
    stre_data = load_image(r"photo/stre.png")
    waves_data = load_image(r"photo/waves.png")
    winds_data = load_image(r"photo/winds.png")
    photo_data = load_image(r"photo/NLC.jpg")
except Exception as e:
    print(f"Критическая ошибка при загрузке изображений: {e}")
    exit(1)

def edit(message: types.Message):
    bot.edit_message_reply_markup(message.chat.id, message.id)

def light_check(call, query):
    edit(call.message)
    bot.send_photo(
        call.message.chat.id, 
        light_data,
        "У серебристых облаков есть своя шкала яркости, чаще всего ее используют при ведении дневника наблюдателя, в идеале этот параметр надо записывать каждые 15-30 минут.",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Назад", callback_data="back")]]
        ))

def back(call, query):
    edit(call.message)
    bot.send_photo(
        call.message.chat.id, 
        photo_data, 
        "Серебристые облака - это сравнительно редкое атмосферное явление, крайне разрежённые облака, состоящие из мелких льдинок, которые подсвечивает солнце. Возникают эти облака в мезосфере под мезопаузой (на высоте 76—85 км над поверхностью Земли) и видимые в глубоких сумерках, непосредственно после заката или перед восходом Солнца.",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Типы СО", callback_data="type_choise")],
             [types.InlineKeyboardButton("Яркость СО", callback_data="light")]]
        )
    )

def types_send_nlc(call, query):
    markup = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Выбрать другой тип", callback_data="type_choise")],
         [types.InlineKeyboardButton("Вернуться к информации о СО", callback_data="back")]]
    )

    bot.delete_message(call.message.chat.id, call.message.id)

    if query[0] == "fler":
        bot.send_photo(
            call.message.chat.id, 
            fler_data, 
            '''Тип I. Флёр
Очень тонкие структуры, не имеющие определенных очертаний, которые часто служат фоном для других облачных форм. Они напоминают слоистые облака, иногда имеют слегка нитевидное строение и зачастую демонстрируют дрожащее свечение. Флёр — это простейшая форма серебристых облаков, часто предшествующая (примерно за полчаса) появлению серебристых облаков с хорошо определенным строением.''',
            reply_markup=markup
        )
    elif query[0] == "str":
        bot.send_photo(
            call.message.chat.id,
            stre_data,
            '''Тип II. Полосы
Длинные линии, часто в группах, расположенные примерно параллельно друг друга или переплетающиеся под малыми углами. Иногда встречаются отдельные полосы. Различают две группы серебристых облаков этого типа:
IIa: состоящие из линий с размытыми нечеткими краями;
IIb: состоящие из линий с хорошо очерченными краями.''',
            reply_markup=markup
        )
    elif query[0] == "waves":
        bot.send_photo(
            call.message.chat.id,
            waves_data,
            '''Тип III. Волны
Короткие полоски, расположенные почти параллельно и с малым интервалом. Расстояние между соседними валами варьируется от 1 до 10 км. Валы проходят перпендикулярно длинным полосам, придавая небосводу вид расчески или птичьего пера, или появляются отдельно от других форм на фоне флёра.''',
            reply_markup=markup
        )
    elif query[0] == "wind":
        bot.send_photo(
            call.message.chat.id,
            winds_data,
            '''Тип IV. Завихрения
Частичные или, в редких случаях, полные кольца облаков с темной серединой. Иногда можно наблюдать во флёре, полосах и валах. Выделяют три группы:
IVa: состоящие из завихрений малого радиуса кривизны (0,1−0,5°);
IVb: представляющие собой изгиб одной или нескольких полос;
IVc: имеющие форму большого кольца.''',
            reply_markup=markup
        )

def type_choise(call, query):
    edit(call.message)
    bot.send_message(
        call.message.chat.id, 
        "Выберите тип, о котором хотите узнать", 
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Флер", callback_data="types fler"),
             types.InlineKeyboardButton("Полосы", callback_data="types str")],
            [types.InlineKeyboardButton("Волны", callback_data="types waves"),
             types.InlineKeyboardButton("Вихри", callback_data="types wind")]]
        ))