import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import SetMyCommands
from dotenv import load_dotenv

from Keyboards.keyboards import UserKeyboards
from Commands.commands import set_commands_Users
from Data.DB import DataBase

DB = DataBase()
UK = UserKeyboards()

load_dotenv()

async def get_start(message: Message, bot: Bot):
    DB.db_add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}.', reply_markup=UK.reply_keyboard())

async def get_help(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Этот бот создан для таго, чтобы напопинать тебе о ежедневных занятиях.\n"Help" - получи помощь.\n"Show today tasks" - узнать, какие сегодня занятия.', reply_markup=UK.reply_keyboard())

async def show_today_tasks(message: Message, bot: Bot):
    day_id = DB.db_get_day_id(message.from_user.id)
    today_tasks = DB.db_show_today_tasks(day_id)
    await bot.send_message(message.from_user.id, today_tasks)
    
async def send_remind_cron_breakfast(bot: Bot):
    all_users = DB.db_all_users()
    for i in all_users:
        breakfast = DB.db_get_breakfast(i[1])
        await bot.send_message(i[0], breakfast)
        
async def send_remind_cron_lunch(bot: Bot):
    all_users = DB.db_all_users()
    for i in all_users:
        lunch = DB.db_get_lunch(i[1])
        await bot.send_message(i[0], lunch)
        
async def send_remind_cron_dinner(bot: Bot):
    all_users = DB.db_all_users()
    for i in all_users:
        print(i[0])
        dinner = DB.db_get_dinner(i[1])
        await bot.send_message(i[0], dinner)
