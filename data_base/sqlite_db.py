import sqlite3 as sq
from create_bot import bot


async def sql_start():
    global base, cur
    base = sq.connect('volonteer_bot.db')
    cur = base.cursor()
    if base:
        print('Data base is connected.')
    base.execute('CREATE TABLE IF NOT EXISTS menu(region TEXT, category TEXT, description TEXT, number TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_message(message.from_user.id, f'Область: {ret[0]}\nКатегорiя: {ret[1]}\nОпис: {ret[2]}\nКонтакт:'
                                                     f' {ret[3]}\nНомер телефону: {ret[-1]}')
