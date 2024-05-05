import asyncio
from datetime import datetime, time, timedelta

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import get_addresses_kb, addresses_list_kb, yes_no_kb, cancel_kb
from services.services import shops
from filters.filters import IsShopKey, IsShopKeyInput
from bot import FSMGetInfo
from database.orm_query import orm_add_user, orm_get_user_by_tg_id, orm_get_day_orders, orm_new_order, orm_get_user_by_id
from config_data.config import load_config

router = Router()
current_shop = {}
send_to_boss_task = None
config = load_config('.env')


# Этот хендлер срабатывает на команду /start
@router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession):
    await message.answer(text=LEXICON_RU['/start'])
    if not await orm_get_user_by_tg_id(session, message.from_user.id):
        await orm_add_user(session, {
            'tg_user_id': message.from_user.id,
            'tg_name': f'{message.from_user.full_name}',
        })


# Этот хендлер срабатывает на команду /help
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хендлер срабатывает на команду /contacts
@router.message(Command('contacts'))
async def contacts_command(message: Message):
    await message.answer(text=LEXICON_RU['/contacts'])


# Этот хендлер срабатывает на команду /service
@router.message(Command('service'))
async def service_command(message: Message):
    await message.answer(text=LEXICON_RU['/service'])


# Этот хендлер срабатывает на команду /replace
@router.message(Command('replace'))
async def replace_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['replace'],
        reply_markup=get_addresses_kb()
    )
    await state.set_state(FSMGetInfo.get_shop)


# Этот хендлер срабатывает на кнопку "Отмена" и сбрасывает состояние FSM
@router.callback_query(F.data == 'cancel')
async def process_press_cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON_RU['/help']
    )
    await state.clear()


# Этот хендлер срабатывает на кнопку "Список адресов" и переводит бота в FSM состояние get_shop
@router.callback_query(F.data == 'addresses_list')
async def process_address_list(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['choose_address'],
        reply_markup=addresses_list_kb(),
    )


# Этот хендлер срабатывает на кнопку с адресом магазина
@router.callback_query(StateFilter(FSMGetInfo.get_shop), IsShopKey())
async def process_shop_button(callback: CallbackQuery, state: FSMContext):
    global current_shop
    await state.update_data(shop=callback.data)
    state_data = await state.get_data()
    shop_num = state_data['shop']
    current_shop = {shop_num: shops[shop_num]}
    await callback.message.edit_text(
        text=f"{LEXICON_RU['is_right_choose']}: {shops[shop_num]}",
        reply_markup=yes_no_kb()
    )


# Этот хендлер срабатывает на сообщение с номером магазина
@router.message(StateFilter(FSMGetInfo.get_shop), IsShopKeyInput())
async def process_shop_button(message: Message, state: FSMContext):
    global current_shop
    await state.update_data(shop=message.text)
    state_data = await state.get_data()
    shop_num = state_data['shop']
    current_shop = {shop_num: shops[shop_num]}
    await message.answer(
        text=f"{LEXICON_RU['is_right_choose']}: {shops[shop_num]}",
        reply_markup=yes_no_kb()
    )


# Этот хендлер срабатывает на кнопку Да в состоянии get_shop
@router.callback_query(StateFilter(FSMGetInfo.get_shop), F.data == 'yes')
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['get_equipment'],
        reply_markup=cancel_kb()
    )
    await state.set_state(FSMGetInfo.get_equipment)


# Этот хендлер срабатывает на кнопку Нет в состоянии get_shop
@router.callback_query(StateFilter(FSMGetInfo.get_shop), F.data == 'no')
async def process_no_button(callback: CallbackQuery, state: FSMContext):
    await replace_command(callback.message, state)


# Этот хендлер срабатывает на ввод текста в состоянии get_equipment
@router.message(StateFilter(FSMGetInfo.get_equipment))
async def process_get_equipment_text(message: Message, session: AsyncSession):
    db_user = await orm_get_user_by_tg_id(session, tg_id=message.from_user.id)
    global current_shop
    shop_num = next(iter(current_shop))
    await orm_new_order(session, db_user.id, {
        'message': message.text,
        'shop_num': int(shop_num),
        'shop_address': current_shop[shop_num]
    })
    await message.answer(
        text=f"{message.text} {LEXICON_RU['replace_equipment']} {current_shop[shop_num]}",
        reply_markup=yes_no_kb()
    )


# Этот хендлер срабатывает на кнопку Да в состоянии get_equipment
@router.callback_query(StateFilter(FSMGetInfo.get_equipment), F.data == 'yes')
async def process_yes_button(callback: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    global send_to_boss_task
    await callback.message.edit_text(
        text=LEXICON_RU['done'],
    )
    await state.clear()
    if send_to_boss_task:
        send_to_boss_task.cancel()
    send_to_boss_task = asyncio.create_task(send_scheduled_orders(bot, session, config.tg_bot.boss_id, time(20, 00)))


# Этот хендлер срабатывает на кнопку Нет в состоянии get_shop
@router.callback_query(StateFilter(FSMGetInfo.get_equipment), F.data == 'no')
async def process_no_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await process_press_cancel(callback, state, bot)


# Хендлер срабатывает на команду /orders и выдает список заказов
@router.message(Command('orders'))
async def process_orders_command(message: Message, session: AsyncSession, bot: Bot):
    if message.from_user.id != config.tg_bot.boss_id:
        await message.answer(text=LEXICON_RU['not_admin'])
    else:
        await message.answer(text=LEXICON_RU['wait'])
        now = datetime.now() + timedelta(seconds=3)
        await send_scheduled_orders(bot, session, config.tg_bot.boss_id, now.time())


# Отправка списка заказов по расписанию
async def send_scheduled_orders(bot: Bot, session: AsyncSession, chat_id: int, send_time: time):
    now = datetime.now().time()
    if now > send_time:
        return
    else:
        while now < send_time:
            await asyncio.sleep(60)
            now = datetime.now().time()
        today = datetime.today()
        start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
        msg = ''
        orders_by_shop = {}
        orders = await orm_get_day_orders(session, start_of_day)
        for order in orders:
            user = await orm_get_user_by_id(session, order.user_id)
            orders_by_shop.setdefault(order.shop_address, []).append((order.message, user.tg_user_name, order.created_at))

        for k, v in orders_by_shop.items():
            msg += f'{k}:\n'
            for data in v:
                msg += f"<code>{data[0]} - {data[1]} - {datetime.strftime(data[2], '%H:%M')}</code>\n"
            msg += f"{'-' * len(k)}\n\n"
        await bot.send_message(chat_id=chat_id, text=msg)
