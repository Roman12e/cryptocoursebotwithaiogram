from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import bot_token, proxy


storage = MemoryStorage()
bot = Bot(bot_token, proxy=proxy)
dp = Dispatcher(bot=bot, storage=storage)


