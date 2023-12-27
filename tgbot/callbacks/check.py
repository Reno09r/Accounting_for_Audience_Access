from aiogram.types import Message
from db.db import Database

async def check(message: Message):
    async with Database() as db:
        username = message.from_user.username
        query = "SELECT * FROM keycontrol_employee WHERE tg_username = $1"
        result = await db.connection.fetchrow(query, username)
    return bool(result)
        