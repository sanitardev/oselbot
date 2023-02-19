from aiogram import executor
from dp import dp, ThrottlingMiddleware
from backup import on_startup
import handlers
from api import app
from threading import Thread


def run_api ():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=80)

if __name__ == "__main__":
    Thread(target=run_api).start()
    print("Bot is starting...")
    dp.setup_middleware(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
