import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from Keyboards.keyboards import AdminKeyboards, UserKeyboards


load_dotenv()

def get_admin(message: Message):
    return int(message.from_user.id) == int(os.getenv('ADMIN_ID'))

def keyboards_(message: Message):
    return AdminKeyboards if get_admin(message) else UserKeyboards


async def get_start(message: Message, bot: Bot):
    # добавить проверку в бд юзера, если нету создать ему с json базу тасков
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}.',
                           reply_markup=keyboards_(message).reply_keyboard())


async def get_help(message: Message, bot: Bot):
    text = 'тут запись админу' if get_admin(message) else 'запись юзеру'
    await bot.send_message(message.from_user.id, text, reply_markup=keyboards_(message).reply_keyboard())

async def show_all_task(message: Message, bot: Bot):
    # добавить код с поиском таксов с бд
    tasks = 'Таски'
    await bot.send_message(message.from_user.id, tasks, reply_markup=keyboards_(message).reply_keyboard())


async def send_remind_cron(bot: Bot):
    pass
    # работа с баззой данных


async def add_time_user(bot: Bot):
    pass
    # код для добавления юзером времени