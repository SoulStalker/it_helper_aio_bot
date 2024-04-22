from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from services.services import shops


class IsShopKey(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit() and str(callback.data) in shops.keys()
