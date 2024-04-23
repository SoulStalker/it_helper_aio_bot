from datetime import datetime

from sqlalchemy import select, update, delete, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Order


# Функция получения пользователя по телеграм id
async def orm_get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User:
    query = select(User).where(User.tg_user_id == tg_id)
    users = await session.execute(query)
    user = users.scalars().first()
    return user


# Функция добавления нового пользователя
async def orm_add_user(session: AsyncSession, user: dict) -> None:
    obj = User(
        tg_user_id=user["tg_user_id"],
        tg_user_name=user["tg_name"]
    )
    session.add(obj)
    await session.commit()

