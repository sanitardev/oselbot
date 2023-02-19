from aiogram.dispatcher.filters import BoundFilter, Filter
import config
from buttons import *
import time


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return message.from_user.id in config.admin_ids


class IsGroupFilter(BoundFilter):
    key = "is_group"

    def __init__(self, is_group: bool):
        self.is_group = is_group

    async def check(self, message: types.Message):
        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            return True
        return False


class IsPrivateFilter(BoundFilter):
    key = "is_private"

    def __init__(self, is_private: bool):
        self.is_group = is_private

    async def check(self, message: types.Message):
        if message.chat.type == 'private':
            return True
        return False


class IsBanFilter(BoundFilter):
    key = "is_ban"

    def __init__(self, is_ban: bool):
        self.is_ban = is_ban

    async def check(self, message: types.Message):
        if message.from_user.id in config.ban_ids:
            return False
        return True