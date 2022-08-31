from aiogram import types, Dispatcher
from create_bot import bot


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'start command')    # /start message


async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'help command')    # /help message


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
