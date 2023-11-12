from connection.connection import dp
from keyboard import keyboard
from aiogram import types


@dp.callback_query_handler(
    lambda callback: callback.data in [
        'change_couple_cripto', 'settings_to_menu'
    ]
)
async def callback_off(callback: types.CallbackQuery):
    if callback.data == 'change_couple_cripto':
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='Введите новую пару криптовалюты.'
        )
    else:
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'Это бот криптоплатформы [CommEX](https://www.commex.com/ru).\n'
                 f'В нём ты каждый день можешь узнавать курс интересующей тебя криптовалюты!',
            reply_markup=keyboard.main_ikb,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

