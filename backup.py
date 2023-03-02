import aioschedule
import asyncio
import os
from zipfile import ZipFile
from dp import bot
from config import all
from config import trades


async def backup():
    while True:
        with ZipFile('backup.zip', 'w') as myzip:
            myzip.write("db/database.db")
        try:
            await bot.send_document(1451300395, open("backup.zip", "rb"))
            os.remove("backup.zip")
        except:
            pass
        else:
            break
        await asyncio.sleep(1.5)


async def flush():
    all.flush()
    trades.flush()


async def scheduler():
    aioschedule.every(5).minutes.do(backup)
    aioschedule.every(15).seconds.do(flush)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
