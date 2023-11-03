from aiogram.types import BotCommand
from aiogram import Bot

async def set_commands_Users(bot: Bot):
    commands = [
        BotCommand(
            command='/start',
            description='Старт.'
        ),
        BotCommand(
            command='/Help',
            description='Узнай функционал бота.'
        ),
        BotCommand(
            command='/Show today tasks',
            description='Запиши треню.'
        )
    ]
    
    await bot.set_my_commands(commands)

async def set_commands_Admin():
    commands = [
        BotCommand(
            command='start',
            description='Старт.'
        ),
        BotCommand(
            command='help',
            description='Узнай функционал бота.'
        )
    ]