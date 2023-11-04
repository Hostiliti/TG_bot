import asyncio
import os
from datetime import datetime, time

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import SetMyCommands
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

from Keyboards.keyboards import UserKeyboards
from Data.DB import DataBase
DB = DataBase()
UK = UserKeyboards()

load_dotenv()

class StepsForm(StatesGroup):
    GET_ANSWER = State()
    GET_FLAG = State()

async def get_start(message: Message, bot: Bot):
    DB.db_add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Ты был зарегистрирован!', reply_markup=UK.reply_keyboard())

async def get_help(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Этот бот создан для таго, чтобы напопинать тебе о ежедневных занятиях.\n"Help" - получи помощь.\n"Show today tasks" - узнай, что сегодня тебя ожидает.\n"Add time" - запиши, когда тебе удобно получать уведоиления', reply_markup=UK.reply_keyboard())

async def add_time(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Пожалуйста, впиши расписание вида: 7:30 13:30 19:30')
    await state.set_state(StepsForm.GET_FLAG)
    
async def add_time_flag(message: Message, bot: Bot, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, f'{message.text} Ты уверен?', reply_markup=UK.reply_keyboard_answer())
        await state.set_state(StepsForm.GET_ANSWER)
        await state.update_data(name=message.text)
    except Exception:
        await bot.send_message(message.from_user.id, f'Что-то не так.')
    
async def add_time_answer(message: Message, bot: Bot, state: FSMContext):
    try:
        if message.text == 'Да':
            context_data = await state.get_data()
            DB.db_add_user_time(message.from_user.id, context_data.get("name").split(' '))
            await bot.send_message(message.from_user.id, f'Готово!')
            await state.clear()
    except Exception:
        await bot.send_message(message.from_user.id, f'Что-то не так.')
    
async def show_today_tasks(message: Message, bot: Bot):
    day_id = DB.db_get_day_id(message.from_user.id)
    today_tasks = DB.db_show_today_tasks(day_id)
    await bot.send_message(message.from_user.id, today_tasks)
    
async def send_remind_interval(bot: Bot):
    all_users = DB.db_all_users()
    for k in all_users:
        u_id, d_id, b, l, d = k[0], k[1], k[2], k[3], k[4]
        def in_min(time):
            time = time.split(':')
            minutes = int(time[0]) * 60 + int(time[1])
            return minutes
        current_time = in_min(datetime.now().time().strftime('%H:%S'))
        if in_min(b) - current_time <= 0 and in_min(b) - current_time >=-10 :
            await bot.send_message(u_id, DB.db_get_task(d_id, 'breakfast'))
            break
        elif in_min(l) - current_time <= 0 and in_min(b) - current_time >=-10:
            await bot.send_message(u_id, DB.db_get_task(d_id, 'lunch'))
            break
        elif in_min(d) - current_time <= 0 and in_min(b) - current_time >=-10:
            await bot.send_message(u_id, DB.db_get_task(d_id, 'dinner'))
            DB.change_user_id(u_id, d_id)
            break
   