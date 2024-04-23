from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import get_addresses_kb, addresses_list_kb, yes_no_kb, cancel_kb
from services.services import shops
from filters.filters import IsShopKey, IsShopKeyInput
from bot import FSMGetInfo

router = Router()
current_shop = None


# Этот хендлер срабатывает на команду /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


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
    current_shop = shops[shop_num]
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
    current_shop = shops[shop_num]
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
async def process_get_equipment_text(message: Message):
    global current_shop
    await message.answer(
        text=f"{message.text} {LEXICON_RU['replace_equipment']} {current_shop}",
        reply_markup=yes_no_kb()
    )


# Этот хендлер срабатывает на кнопку Да в состоянии get_equipment
@router.callback_query(StateFilter(FSMGetInfo.get_equipment), F.data == 'yes')
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['done'],
    )
    await state.clear()


# Этот хендлер срабатывает на кнопку Нет в состоянии get_shop
@router.callback_query(StateFilter(FSMGetInfo.get_equipment), F.data == 'no')
async def process_no_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await process_press_cancel(callback, state, bot)
