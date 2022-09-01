from aiogram import types, Dispatcher
from create_bot import bot

from inline_buttons import obl, category, list_obl, list_category


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                 'надання допомоги людям. Натиснiть або "Потрiбна допомога" для '
                                                 'залишення заяви на допомогу.', reply_markup=obl)


async def current_obl(query: types.CallbackQuery):
    cur_obl = query.data
    text = 'Error. Please restart bot'
    for i in range(len(list_obl)):
        if cur_obl == list_obl[i]:
            text = 'Оберiть категорiю:'
    await bot.send_message(query.from_user.id, text, reply_markup=category)


async def current_category(query: types.CallbackQuery):
    cur_category = query.data
    text = 'Error. Please restart bot'
    for i in range(len(list_category)):
        if cur_category == list_category[i]:
            text = 'Опишiть що саме вам потрiбно з цiєї категорiї:'
    await bot.send_message(query.from_user.id, text)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    for i in range(len(list_obl)):
        dp.register_callback_query_handler(current_obl, text=list_obl[i])
    for i in range(len(list_category)):
        dp.register_callback_query_handler(current_category, text=list_category[i])
