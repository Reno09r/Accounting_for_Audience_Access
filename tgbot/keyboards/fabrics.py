from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int

class Choose(CallbackData, prefix="cho"):
    action: str
    name: str

def paginator(names: list, page: int = 0, items_per_page: int = 8, pagination_btns: bool = True,  search_btn: bool = True):
    start_index = page * items_per_page
    end_index = (page + 1) * items_per_page

    builder = InlineKeyboardBuilder()

    for name in names[start_index:end_index]:
        builder.row(
            InlineKeyboardButton(text=name, callback_data=Choose(action="clicked", name=name).pack()),
            width=1,
        )

    if pagination_btns:
        builder.row(
            InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev", page=page - 1).pack()),
            InlineKeyboardButton(text="➡", callback_data=Pagination(action="next", page=page + 1).pack())
        )
    if search_btn:
        builder.row(
            InlineKeyboardButton(text="Поиск", callback_data='search'),
        )
    return builder.as_markup()

