from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from inline_buttons import obl, category, agree_buttons, list_obl, list_category


class FSMClient(StatesGroup):
    region_state = State()
    category_state = State()
    description_state = State()
    contact_state = State()
    number_state = State()


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вiтаю, ви почали роботу з ботом волонтером, який створенний для '
                                                 'надання допомоги людям. Натиснiть або "Потрiбна допомога" для '
                                                 'залишення заяви на допомогу.', reply_markup=obl)


async def current_obl(query: types.CallbackQuery, state: FSMContext):
    cur_obl = query.data
    await FSMClient.region_state.set()
    async with state.proxy() as data:
        data['region_state'] = cur_obl
    await FSMClient.next()
    await bot.send_message(query.from_user.id, 'Оберiть категорiю:', reply_markup=category)


async def current_category(query: types.CallbackQuery, state: FSMContext):
    cur_category = query.data
    async with state.proxy() as data:
        data['category_state'] = cur_category
    await FSMClient.next()
    await bot.send_message(query.from_user.id, 'Опишiть що саме вам потрiбно з цiєї категорiї:')


async def input_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description_state'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, "Залишити контакт?", reply_markup=agree_buttons)


async def input_contact(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'yes':
        async with state.proxy() as data:
            data['contact_state'] = query.from_user.id
    else:
        async with state.proxy() as data:
            data['contact_state'] = ''
    await FSMClient.next()
    await bot.send_message(query.from_user.id, "Напишiть номер телефону для зв'язку з вами:")


async def input_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_state'] = message.text
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, str(data))
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    for i in range(len(list_obl)):
        dp.register_callback_query_handler(current_obl, text=list_obl[i], state=None)
    for i in range(len(list_category)):
        dp.register_callback_query_handler(current_category, text=list_category[i], state=FSMClient.category_state)
    dp.register_message_handler(input_description, state=FSMClient.description_state)
    dp.register_callback_query_handler(input_contact, text='yes', state=FSMClient.contact_state)
    dp.register_callback_query_handler(input_contact, text='no', state=FSMClient.contact_state)
    dp.register_message_handler(input_number, state=FSMClient.number_state)
