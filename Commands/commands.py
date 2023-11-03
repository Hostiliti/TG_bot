from aiogram.types import BotCommand
from aiogram import Bot

async def set_commands_Users(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Старт.'
        ),
        BotCommand(
            command='help',
            description='Узнай функционал бота.'
        ),
        BotCommand(
            command='write_training',
            description='Запиши треню.'
        ),
        BotCommand(
            command='del_training',
            description='Удали треню, если она отменилась.'
        ),
        BotCommand(
            command='show_all',
            description='Посмотри, какие трени записаны.'
        )
    ]

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