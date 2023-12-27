from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Передача ключей"),
            KeyboardButton(text="Доступные ключи")
        ],
        [
            KeyboardButton(text="Имеющиеся ключи")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зарегистрироваться"),
        ],
    ],
    resize_keyboard=True
)
