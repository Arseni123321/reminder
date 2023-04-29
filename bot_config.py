import asyncio
import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from handlers import reminder, other, bug_report
from config import load_congig
from database.sqlite_db import SQLiteDB

storage = MemoryStorage()
logger = logging.getLogger(__name__)

config = load_congig(r'config/config.ini')

TOKEN = config.tg_bot.BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

DB = SQLiteDB()


async def set_commands(bot: Bot):
    """Установка команд для бота

    :param bot:
    :return:
    """
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/cancel', description='Отмена'),
        BotCommand(command='/bug_report', description='Отправить сообщение'),
    ]

    await bot.set_my_commands(commands)


async def main():
    logging.info('Bot started')

    reminder(dp)

    await set_commands(bot=bot)
    await dp.start_polling()


if __name__ == '__main__':
    #asyncio.run(main())
    logging.info()