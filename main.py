from aiogram import executor
from dp import dp, ThrottlingMiddleware
from backup import on_startup
import handlers

if __name__ == "__main__":
    print("Bot is starting...")
    dp.setup_middleware(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
