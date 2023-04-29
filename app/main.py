import asyncio
import logging

from aiogram import types, Dispatcher, Bot
from aiogram.types import BotCommand
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status
from bot_config import dp, bot, TOKEN, logger, config,DB
from handlers import bug_report, reminder, other

