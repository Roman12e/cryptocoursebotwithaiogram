from aiogram.dispatcher.filters.state import State, StatesGroup
from connection.connection import dp, bot
from aiogram.dispatcher import FSMContext
from database.db import conn, cur

from aiogram import types
from binance import Client

from keyboard import keyboard
from settings import api_key, api_secret

list_of_cripto = []

client = Client(
    api_key,
    api_secret,
    testnet=True
)


admin_1 = 972244742
new_user_id = ''

help_text = """
/start --> <em>Перезапуск бота</em>
/questions --> <em>Если есть какие-то вопросы или пожелания, то можете их написать</em>
"""


class GetQuestionsUser(StatesGroup):

    questions = State()
    answer = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global admin_1
    cur.execute(("""CREATE TABLE IF NOT EXISTS user_profile (
        user_id_chat TEXT PRIMARY KEY,
        name text,
        user_cripto text 
    )"""))
    conn.commit()

    user_name = message.from_user.full_name
    user_id = message.chat.id
    cur.execute("SELECT * FROM user_profile WHERE user_id_chat = ?", (user_id,))
    result = cur.fetchone()
    if not result:
        cur.execute("INSERT INTO user_profile VALUES(?, ?, ?)", (user_id, user_name, 'BTCUSDT'))
        conn.commit()
    await message.answer(
            text=f'Приветствую, {message.from_user.full_name}!\n\n'
            f'Это бот криптоплатформы [CommEX](https://www.commex.com/ru).\n'
            f'В нём ты каждый день можешь узнавать курс интересующей тебя криптовалюты!',
            reply_markup=keyboard.main_ikb,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )


@dp.message_handler(commands=['questions'])
async def user_questions(message: types.Message):
    await message.answer('Сюда ты можешь написать свой вопрос или пожелание.')
    await GetQuestionsUser.questions.set()


@dp.message_handler(content_types=['text'], state=GetQuestionsUser.questions)
async def send_questions(message: types.Message, state: FSMContext):
    global admin_1
    async with state.proxy() as data:
        data['questions'] = message.text

        await bot.send_message(
            chat_id=admin_1,
            text=f"Пользователь {message.from_user.full_name}\n"
                 f"С ID: {message.from_user.id}\n"
                 f"Отправил сообщение: {data['questions']}"
        )
        await message.answer(
            'Ваше сообщение успешно отправлено!',
            reply_markup=keyboard.main_ikb
        )
        await GetQuestionsUser.next()


@dp.message_handler(commands=['answer'])
async def answer(message: types.Message):
    await message.answer('Отправь мне ID того кому хочешь отправить сообщение')


@dp.message_handler(lambda message: message.text.isdigit())
async def get_id(message: types.Message):
    global new_user_id
    new_user_id = message.text
    await message.answer('Теперь напиши сообщение')
    await GetQuestionsUser.answer.set()


@dp.message_handler(lambda message: message.text.capitalize(), state=GetQuestionsUser.answer)
async def send_answer(message: types.Message, state: FSMContext):
    global new_user_id
    async with state.proxy() as data:
        data['answer'] = message.text
        await bot.send_message(
            chat_id=new_user_id,
            text=data['answer']
        )
        await message.answer('Сообщение успешно отправлено!')

    await state.finish()

