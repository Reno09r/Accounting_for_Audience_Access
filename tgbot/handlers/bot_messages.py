from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from callbacks import check
from aiogram.fsm.context import FSMContext
from db.db import get_keyless_employees, get_free_audience, have_a_key
from keyboards import reply, fabrics
from utils.states import RegistrationState
router = Router()

async def free_auditoriums_message():
    auds = await get_free_audience()
    message = f"Доступные ключи: {', '.join(auds)}"
    return message

    

@router.message()
async def echo(message: Message, state: FSMContext):
    res = await check.check(message)
    if res or message.text == "Зарегистрироваться":
        emps = await get_keyless_employees()
        msg = message.text

        if msg == "Имеющиеся ключи":
            keys = await have_a_key(message.from_user.username)
            if keys:
                keys_str = ', '.join(keys)
                await message.answer(f"Ваши ключи: {keys_str}", reply_markup=None)
            else:
                await message.answer(f"У вас нету ключей!")
        elif msg == "Зарегистрироваться":
            if not res: 
                await state.set_state(RegistrationState.entering_card_id)
                await message.answer("Введите ID своей карточки:", reply_markup=ReplyKeyboardRemove())
            else: 
                await message.answer("Вы уже в системе! Вам незачем снова регистрироваться.", reply_markup=reply.main)
        elif msg == "Доступные ключи":
            response_message = await free_auditoriums_message()
            await message.answer(response_message)
        elif msg == "Передача ключей":
            if await have_a_key(message.from_user.username):
                await message.answer(f"Передать ключи сотруднику: ", reply_markup=fabrics.paginator(emps))
            else:
                await message.answer(f"У вас нету ключей!")
    else:
        await message.answer("Вы не в системе.", reply_markup=reply.register)

        