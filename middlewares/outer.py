from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import async_sessionmaker


# Мидльваря тихо блокирует всех юзеров кроеме тех, которые прописаны в списке админов в файле .env
class ShadowBanMiddleware(BaseMiddleware):

    def __init__(self, admins):
        self.admins = admins

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        user: User = data.get('event_from_user')
        if user is not None:
            if not user.id in self.admins:
                return

        return await handler(event, data)


# Класс для подключения базы данных
class DbMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)

