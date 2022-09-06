from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from inline_buttons import obl, category, agree_buttons, need_help_button, your_statement_button, list_obl, \
    list_category


class FSMClient(StatesGroup):
    start_state = State()
    need_help = State()
    region_state = State()
    category_state = State()
    description_state = State()
    number_state = State()
    your_statement_state = State()


chat_id = '-1001729485030'


async def command_start(message: types.Message):
    await FSMClient.start_state.set()
    await bot.send_message(message.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                 'надання допомоги людям. Залиште заяву на допомогу',
                           reply_markup=need_help_button)
    await FSMClient.next()


async def need_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Оберiть область в якiй потрiбна допомога:', reply_markup=obl)
    await FSMClient.next()


async def current_obl(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        await FSMClient.start_state.set()
        await bot.send_message(query.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                   'надання допомоги людям. Оберiть область в якiй потрiбна допомога:',
                               reply_markup=need_help_button)
        await FSMClient.next()
    else:
        async with state.proxy() as data:
            data['region_state'] = query.data
        await FSMClient.next()
        await bot.send_message(query.from_user.id, 'Оберiть категорiю:', reply_markup=category)


async def current_category(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        await FSMClient.start_state.set()
        await bot.send_message(query.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                   'надання допомоги людям. Оберiть область в якiй потрiбна допомога:',
                               reply_markup=need_help_button)
        await FSMClient.next()
    else:
        async with state.proxy() as data:
            data['category_state'] = query.data
        await FSMClient.next()
        await bot.send_message(query.from_user.id, 'Опишiть що саме вам потрiбно з цiєї категорiї:')


async def input_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description_state'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, "Залишити номер телефону?", reply_markup=agree_buttons)


async def enter_number(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        await FSMClient.start_state.set()
        await bot.send_message(query.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                   'надання допомоги людям. Оберiть область в якiй потрiбна допомога:',
                               reply_markup=need_help_button)
        await FSMClient.next()
    else:
        if query.data == 'yes':
            await bot.send_message(query.from_user.id, "Напишiть ваш номер телефону для звя'зку:")
        else:
            async with state.proxy() as data:
                data['number_state'] = ''
            await sqlite_db.sql_delete()
            await sqlite_db.sql_add_command(state)
            await bot.send_message(query.from_user.id, 'Ваша заява:')
            await sqlite_db.sql_read(query)
            await bot.send_message(query.from_user.id, 'Все вiрно?', reply_markup=your_statement_button)
            await FSMClient.next()


async def input_number(message: types.Message, state: FSMContext):
    number_list = list(message.text)
    count_int_num = 0
    for i in range(1, len(number_list)):
        if number_list[i].isnumeric():
            count_int_num += 1
    if (number_list[0] == '+' and count_int_num == 12) or (message.text.isnumeric() and (len(number_list) == 10)
                                                           or len(number_list) == 12):
        async with state.proxy() as data:
            data['number_state'] = message.text
        await sqlite_db.sql_delete()
        await sqlite_db.sql_add_command(state)
        await bot.send_message(message.from_user.id, 'Ваша заява:')
        await sqlite_db.sql_read(message)
        await bot.send_message(message.from_user.id, 'Все вiрно?', reply_markup=your_statement_button)
        await FSMClient.next()
    # if message.text.isnumeric():
    #     async with state.proxy() as data:
    #         data['number_state'] = message.text
    #     await sqlite_db.sql_delete()
    #     await sqlite_db.sql_add_command(state)
    #     await bot.send_message(message.from_user.id, 'Ваша заява:')
    #     await sqlite_db.sql_read(message)
    #     await bot.send_message(message.from_user.id, 'Все вiрно?', reply_markup=your_statement_button)
    #     await FSMClient.next()
    else:
        await bot.send_message(message.from_user.id, 'Номер введено неккоректно. Ввести номер ще раз?.',
                               reply_markup=agree_buttons)
        await FSMClient.number_state.set()


async def edit(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'yes':
        await bot.send_message(query.from_user.id, 'Ваша заява залишена, зачекайте поки хтось вiдгукнеться!'
                                                   '\nДякуємо за використання бота.')
        await bot.send_message(query.from_user.id, 'Ви також можете допомогти комусь в цьому телеграм каналi:'
                                                   '\nhttps://t.me/volonteer_bot_need_help')
        await sqlite_db.sql_commit(chat_id)
        await state.finish()
    else:
        await FSMClient.start_state.set()
        await bot.send_message(query.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                   'надання допомоги людям. Оберiть область в якiй потрiбна допомога:',
                               reply_markup=need_help_button)
        await FSMClient.next()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_callback_query_handler(need_help, text='need_help', state=FSMClient.need_help)

    for i in range(len(list_obl)):
        dp.register_callback_query_handler(current_obl, text=list_obl[i], state=FSMClient.region_state)
    dp.register_callback_query_handler(current_obl, text='back', state=FSMClient.region_state)

    for i in range(len(list_category)):
        dp.register_callback_query_handler(current_category, text=list_category[i], state=FSMClient.category_state)
    dp.register_callback_query_handler(current_category, text='back', state=FSMClient.category_state)

    dp.register_message_handler(input_description, state=FSMClient.description_state)

    dp.register_callback_query_handler(enter_number, text='yes', state=FSMClient.number_state)
    dp.register_callback_query_handler(enter_number, text='no', state=FSMClient.number_state)
    dp.register_callback_query_handler(enter_number, text='back', state=FSMClient.number_state)

    dp.register_message_handler(input_number, state=FSMClient.number_state)
    dp.register_callback_query_handler(edit, state=FSMClient.your_statement_state)
