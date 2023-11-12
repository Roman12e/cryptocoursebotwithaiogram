from aiogram import executor

if __name__ == '__main__':
    from callback import dp
    from maincmd import dp
    executor.start_polling(
        dp, skip_updates=True
    )
