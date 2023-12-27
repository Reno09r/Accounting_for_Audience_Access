import random

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from callbacks import check
from db.db import Database
from keyboards import reply
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    res = await check.check(message)
    
    if res:
        await message.answer("Добро пожаловать!", reply_markup=reply.main)
    else:
        await message.answer("Вы не в системе.", reply_markup=reply.register)
