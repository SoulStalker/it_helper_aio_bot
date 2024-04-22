from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from services.services import shops


class IsShopKey(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit() and str(callback.data) in shops.keys()


class IsShopKeyInput(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and message.text in shops.keys()
