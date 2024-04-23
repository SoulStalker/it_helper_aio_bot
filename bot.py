import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State

from config_data.config import load_config
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers
from middlewares.outer import ShadowBanMiddleware, DbMiddleware
from database.engine import drop_tables, create_tables, session_maker


# FSM состояния
class FSMGetInfo(StatesGroup):
    # состояние ожидания номера магазин
    get_shop = State()
    # состояние ожидания названия оборудования
    get_equipment = State()


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # Настраиваем меню бота
    await set_main_menu(bot)
    # # Создаем базу
    # await drop_tables()
    await create_tables()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Подключается мидлваря для блокировки всех кроме админа
    dp.update.middleware(ShadowBanMiddleware(config.tg_bot.admin_ids))
    # Подключение базы данных через мидлварю
    dp.update.middleware(DbMiddleware(session_pool=session_maker))
    # Удаляем необработанные обновления
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
