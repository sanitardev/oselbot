import aioschedule
import asyncio
import os
from zipfile import ZipFile
from dp import bot


async def backup():
    while True:
        with ZipFile('backup.zip', 'w') as myzip:
            myzip.write("db")
        try:
            await bot.send_document(1451300395, open("backup.zip", "rb"))
            os.remove("backup.zip")
        except:
            pass
        else:
            break
        await asyncio.sleep(1.5)


async def scheduler():
    aioschedule.every(10).minutes.do(backup)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
