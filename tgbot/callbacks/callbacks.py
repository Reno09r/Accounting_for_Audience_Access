from contextlib import suppress
from datetime import datetime
from db.db import Database, get_employee_has_not_taken_key, have_a_key, have_a_key_full_table, insert_into_byemptakedkey, insert_into_keytransfer, reg_check, register_tg_user, search_employee, update_byemptakedkey
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import math
from keyboards import fabrics, reply
from utils.states import RegistrationState, SearchState

router = Router()

@router.callback_query(fabrics.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: fabrics.Pagination):
    emps = await get_employee_has_not_taken_key(call.from_user.username)
    page_num = int(callback_data.page)
    max_page = math.ceil((len(emps) - 1) / 8 )
    if callback_data.action == "next":
        page = min(page_num + 1, max_page) - 1
    elif callback_data.action == "prev":
        page = max(page_num, 0)
    else:
        page = page_num


    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"Передать ключи сотруднику:",
            parse_mode='HTML',
            reply_markup=fabrics.paginator(emps, page)
        )
    await call.answer()

@router.callback_query(fabrics.Choose.filter(F.action.in_(["clicked"])))
async def choose_handler(call: CallbackQuery, callback_data: fabrics.Choose):
    last_name, first_name = callback_data.name.split()
    rows = await have_a_key_full_table(call.from_user.username)
    for row in rows:
        aud_id, from_emp_id = row.split()
        await insert_into_keytransfer(int(from_emp_id), last_name, first_name, int(aud_id), datetime.now())
        await insert_into_byemptakedkey(last_name, first_name, int(aud_id), call.from_user.username)
        await update_byemptakedkey(call.from_user.username)
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"Вы передали ключи сотруднику {last_name} {first_name}",
            parse_mode='HTML',
            reply_markup=None) 
    await call.answer()

@router.callback_query(F.data == "search")
async def choose_handler(call: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"Введите ФИО (Фамилия, инициалы): ",
            parse_mode='HTML',
            reply_markup=None) 
    await state.set_state(SearchState.searching)

    await call.answer()

@router.message(RegistrationState.entering_card_id)
async def handle_registration(message: Message, state: FSMContext):
    rows = await reg_check(message.text)
    if rows:
        await register_tg_user(message.from_user.username, rows[0]["id"])
        await message.answer("Вы успешно зарегистрированы!", reply_markup=reply.main) 
    else:
        await message.answer("Вы не были зарегистрированы, ID карточки неправильный либо уже по этой ID карточке был зарегистрирован пользователь.", reply_markup=reply.register) 
    await state.clear()
@router.message(SearchState.searching)

async def handle_search_query(message: Message, state: FSMContext):
    search_query = message.text
    emps = await search_employee(search_query, message.from_user.username)
    page_num = 0  
    with suppress(TelegramBadRequest):
        if emps:
            await message.answer(
                f"Результаты поиска для '{search_query}':",
                parse_mode='HTML',
                reply_markup=fabrics.paginator(emps, page_num, search_btn=True, pagination_btns=False)
            )
        else:
            await message.answer(
                f"Результаты поиска для '{search_query}':",
                parse_mode='HTML',
                reply_markup=fabrics.paginator(emps, page_num, search_btn=False, pagination_btns=False)
            )
    await state.clear()
