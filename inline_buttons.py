from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_obl = ['АР Крим', 'Вінницька', 'Волинська', 'Дніпропетровська', 'Донецька', 'Житомирська', 'Закарпатська',
            'Запорізька'
            'Івано-Франківська', 'Київська', 'Кіровоградська', 'Луганська', 'Львівська', 'Миколаївська', 'Одеська',
            'Полтавська', 'Рівненська', 'Сумська', 'Тернопільська', 'Харківська', 'Херсонська', 'Хмельницька',
            'Черкаська', 'Чернівецька', 'Чернігівська']

list_category = ['Робоча сила', 'Перевезення', 'Продукти', 'Одяг', 'Лiки', 'Житло', 'Iнше']

need_help_button = InlineKeyboardMarkup(row_width=1)
need_help = InlineKeyboardButton('Залишити заяву на допомогу', callback_data='need_help')
need_help_button.add(need_help)

go_back_button = InlineKeyboardMarkup(row_width=1)
go_back = InlineKeyboardButton('Повернутись', callback_data='back')
go_back_button.add(go_back)

obl = InlineKeyboardMarkup(row_width=1)
for i in range(len(list_obl)):
    obl_button = InlineKeyboardButton(list_obl[i], callback_data=list_obl[i])
    obl.add(obl_button)
obl.add(go_back)

category = InlineKeyboardMarkup(row_width=1)
for i in range(len(list_category)):
    category_button = InlineKeyboardButton(list_category[i], callback_data=list_category[i])
    category.add(category_button)
category.add(go_back)

agree_buttons = InlineKeyboardMarkup(row_width=2)
button_yes = InlineKeyboardButton('Так', callback_data='yes')
button_no = InlineKeyboardButton('Нi', callback_data='no')
agree_buttons.add(button_yes, button_no, go_back)
