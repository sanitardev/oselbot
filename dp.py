import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled, RetryAfter
from config import token
from utils import *
import logging
from filters import IsAdminFilter, IsGroupFilter, IsBanFilter, IsPrivateFilter
import time
from collections import deque

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ut = Utils()

dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsGroupFilter)
dp.filters_factory.bind(IsBanFilter)
dp.filters_factory.bind(IsPrivateFilter)


class Dialog(StatesGroup):
    posting = State()


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.reply(bold(f"{mention(message)}, не флуди :)"))


@dp.errors_handler(exception=RetryAfter)
async def exception_handler(update: types.Update, exception: RetryAfter):
    try:
        user = update.message.from_user.id
        who = await bot.get_chat_member(update.message.chat.id, user)
        logging.warning(f"Спам от {who}")
    except:
        pass


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator

def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=2, key_prefix='antiflood_', max_requests: int = 1, time_period: int = 3):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.max_requests = max_requests
        self.time_period = time_period
        self.requests = deque()
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data, *args):
        now = time.time()
        while self.requests and self.requests[0] < now - self.time_period:
            self.requests.popleft()
        if len(self.requests) >= self.max_requests:
            await query.answer(f"❗️ таймаут нажатий {self.time_period} секунды ❗️", show_alert=True)
            raise CancelHandler()
        self.requests.append(now)

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            pass

        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)