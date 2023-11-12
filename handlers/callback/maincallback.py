from connection.connection import dp, bot
from datetime import datetime, timedelta
from aiogram import types
from database.db import cur, conn

from keyboard import keyboard
from binance import Client
from apikey import apikey

import asyncio


list_of_cripto = []

client = Client(
    apikey.api_key,
    apikey.api_secret,
    testnet=True
)

admin_1 = 972244742
off_mode = True

help_text = """
/start --> <em>Перезапуск бота</em>
/questions --> <em>Если есть какие-то вопросы или пожелания, то можете их написать</em>
"""


intervals = {
    'one_minute': (Client.KLINE_INTERVAL_1MINUTE, timedelta(seconds=60)),
    'fifteen_minute': (Client.KLINE_INTERVAL_15MINUTE, timedelta(seconds=900)),
    'thirty_minute': (Client.KLINE_INTERVAL_30MINUTE, timedelta(seconds=1800)),
    'one_hour': (Client.KLINE_INTERVAL_1HOUR, timedelta(seconds=3600)),
    'four_hour': (Client.KLINE_INTERVAL_4HOUR, timedelta(seconds=14400))
}
list_of_kline = list(intervals.keys())


@dp.message_handler(regexp=r'^[A-Z]+$')
async def get_new_user_cripto(message: types.Message):
    global list_of_cripto
    user_cripto = message.text.upper()
    user_id = message.chat.id
    exchange_info = client.get_exchange_info()
    for symbol in exchange_info['symbols']:
        list_of_cripto.append(symbol['symbol'])
    if user_cripto in list_of_cripto:
        cur.execute("UPDATE user_profile SET user_cripto = ? WHERE user_id_chat = ?", (user_cripto, user_id))
        conn.commit()
        await message.answer('Вы успешно изменили пару криптовалюты!', reply_markup=keyboard.main_ikb)
    else:
        await message.answer('Такой пары криптовалюты нет!')


@dp.callback_query_handler(
    lambda callback: callback.data in ['help', 'info_cripto', 'follow_mode', 'profile', 'settings']
)
async def main_callback(callback: types.CallbackQuery):
    user_chat_id = callback.message.chat.id
    cripto = cur.execute("SELECT user_cripto FROM user_profile WHERE user_id_chat = ?", (user_chat_id,)).fetchone()
    user_cripto = cripto[0]
    if callback.data == 'help':
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=help_text,
            parse_mode='HTML',
            reply_markup=keyboard.main_ikb
        )

    elif callback.data == 'info_cripto':
        try:
            ticker = client.get_ticker(symbol=user_cripto)
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text=f'В данный момент используется: {user_cripto}.\n'
                     f'Чтобы изменить: <b>Настройки/Изменить криптовалюту</b>.\n\n'
                     f'<em>Информация о паре {user_cripto}.</em>\n'
                     f'Курс на данный момент: {float(ticker["lastPrice"])}\n'
                     f'Максимальная стоимость за последние 24 часа: {float(ticker["highPrice"])}\n'
                     f'Минимальная стоимость за последние 24 часа: {float(ticker["lowPrice"])}\n'
                     f'Цена открытия за последние 24 часа: {float(ticker["openPrice"])}\n'
                     f'Лучшая цена предложения покупки: {float(ticker["bidPrice"])}\n',
                reply_markup=keyboard.main_ikb,
                parse_mode='HTML'
            )
        except KeyError:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text='Упс... что-то пошло не так:('
            )

    elif callback.data == 'follow_mode':
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'Для изменения пары криптовалюты на другую - перейдите: <b>Настройки/Изменить криптовалюту</b>.\n'
                 f'В данный момент используется: {user_cripto}.\n\n'
                 'Режим слежки - режим в котором бот следит за криптовалютой и сообщает вам о её '
                 'изменении через определённое время.\n'
                 'Просто выбери нужный интервал времени, '
                 'с которым бот будет присылать информацию об изменении криптовалюты.',
            reply_markup=keyboard.ikb_time,
            parse_mode='HTML'
        )

    elif callback.data == 'profile':
        profile = cur.execute("SELECT * FROM user_profile WHERE user_id_chat = ?", (user_chat_id,)).fetchone()
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'<em>{"Профиль":.^80}</em>\n'
                 f'<b>Имя --> {profile[1]}</b>\n'
                 f'<b>ID --> {profile[0]}</b>\n'
                 f'<b>Криптовалюта --> {profile[2]}</b>\n',
            reply_markup=keyboard.main_ikb,
            parse_mode='HTML'
        )

    else:
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='Настройки.\nЗдесь ты можешь подстроить бота под себя.',
            reply_markup=keyboard.ikb_user_settings
        )


@dp.callback_query_handler(lambda callback: callback.data in list_of_kline or callback.data == 'off')
async def callback_follow(callback: types.CallbackQuery):
    global off_mode
    user_id_chat = callback.message.chat.id
    cripto = cur.execute("SELECT user_cripto FROM user_profile WHERE user_id_chat = ?", (user_id_chat,)).fetchone()
    user_cripto = cripto[0]
    try:
        if callback.data == 'off':
            off_mode = False
            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text='Режим успешно отключился!',
                reply_markup=keyboard.main_ikb
            )
        else:
            ticker = client.get_ticker(symbol=user_cripto)
            interval = intervals[callback.data]
            while off_mode:
                history_kline = client.get_historical_klines(
                    symbol=user_cripto,
                    interval=interval[0],
                    limit=1
                )
                current_price = float(ticker['lastPrice'])
                past_price = float(history_kline[0][4])
                percent = past_price * 100 / current_price - 100
                await callback.message.answer(
                    f'Цена торговой пары {user_cripto} изменилась на:\n<b>{round(percent, 7)}%</b>\n\n'
                    f'Время: {datetime.now() - interval[1]}\n'
                    f'Было: {past_price}\n\n'
                    f'Время: {datetime.now()}\n'
                    f'Стало: {current_price}',
                    reply_markup=keyboard.ikb_off,
                    parse_mode='HTML'
                )
                await asyncio.sleep(interval[1].total_seconds())
    except KeyError:
        await callback.message.answer('Упс... что-то пошло не так:(')
