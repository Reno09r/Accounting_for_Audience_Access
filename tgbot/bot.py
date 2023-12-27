import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages, user_commands
from callbacks import callbacks
from config_reader import config


async def main():
    bot = Bot(config.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        callbacks.router,
        bot_messages.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())