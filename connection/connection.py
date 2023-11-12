from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apikey.apikey import bot_token

storage = MemoryStorage()
bot = Bot(bot_token)
dp = Dispatcher(bot=bot, storage=storage)


