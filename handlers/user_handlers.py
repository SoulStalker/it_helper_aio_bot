import asyncio
import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User

from lexicon.lexicon import LEXICON_RU

router = Router()


@router.message(CommandStart)
async def send_message(message: Message):
    await message.answer(text=LEXICON_RU['/start'])