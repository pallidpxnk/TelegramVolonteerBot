from aiogram import types, Dispatcher
from create_bot import bot

from inline_buttons import obl


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                 'надання допомоги людям. Натиснiть або "Потрiбна допомога" для '
                                                 'залишення заяви на допомогу', reply_markup=obl)


async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'help command')    # /help message


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
