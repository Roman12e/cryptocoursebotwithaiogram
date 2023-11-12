from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_ikb = InlineKeyboardMarkup(row_width=2)
button_help = InlineKeyboardButton('Помощь', callback_data='help')
button_info_cripto = InlineKeyboardButton('Курс', callback_data='info_cripto')
button_to_follow_cripto = InlineKeyboardButton('Режим слежки', callback_data='follow_mode')
button_profile = InlineKeyboardButton('Профиль', callback_data='profile')
button_settings = InlineKeyboardButton('Настройки', callback_data='settings')
main_ikb.add(button_info_cripto, button_to_follow_cripto).add(button_help, button_profile).add(button_settings)

# mode off
ikb_off = InlineKeyboardMarkup(row_width=1)
button_off = InlineKeyboardButton('Выключить', callback_data='off')
ikb_off.add(button_off)

# for time interval
ikb_time = InlineKeyboardMarkup(row_width=2)
button_one = InlineKeyboardButton('Одна минута', callback_data='one_minute')
button_fifteen = InlineKeyboardButton('Пятнадцать минут', callback_data='fifteen_minute')
button_thirty = InlineKeyboardButton('Тридцать минут', callback_data='thirty_minute')
button_hour = InlineKeyboardButton('Один час', callback_data='one_hour')
button_four_hour = InlineKeyboardButton('Четыре часа', callback_data='four_hour')
ikb_time.add(button_one).add(button_fifteen, button_thirty).add(button_hour, button_four_hour)

# settings couple_cripto
ikb_user_settings = InlineKeyboardMarkup(row_width=1)
button_couple_cripto = InlineKeyboardButton('Изменить криптовалюту', callback_data='change_couple_cripto')
button_back = InlineKeyboardButton('Назад', callback_data='settings_to_menu')
ikb_user_settings.add(button_couple_cripto, button_back)

