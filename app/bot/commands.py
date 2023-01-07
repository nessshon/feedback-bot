import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.utils import markdown
from aiogram.types import (BotCommand, BotCommandScopeAllPrivateChats,
                           BotCommandScopeAllGroupChats, Message)

from app.database.models.users import UserModel

from .texts import Text
from .filters import IsPrivate, IsGroup
from .misc import delete_message, rate_limit


@rate_limit(1)
async def command_start(message: Message):
    if not await UserModel.is_exists(message.from_user.id):
        await UserModel.add(
            id=message.from_user.id,
            name=message.from_user.first_name
        )

    emoji = await message.answer("👋")

    await delete_message(message)
    await asyncio.sleep(1.8)

    user_link = markdown.hlink(
        title=message.from_user.first_name,
        url=message.from_user.url
    )
    text = Text().get_message("START").format(user_link)

    with suppress(Exception):
        await emoji.edit_text(text)


@rate_limit(1)
async def command_id(message: Message):
    await message.reply(markdown.hcode(message.chat.id))


@rate_limit(1)
async def command_source(message: Message):
    emoji = await message.answer("👨‍💻")

    await delete_message(message)
    await asyncio.sleep(1.8)

    text = Text().get_message("SOURCE")

    with suppress():
        await emoji.edit_text(text)


async def setup(bot: Bot):
    commands = {
        "en": [
            BotCommand("start", "Restart"),
            BotCommand("source", "Source code"),
        ],
        "ru": [
            BotCommand("start", "Перезапустить"),
            BotCommand("source", "Исходный код"),
        ]
    }

    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )

    group_commands = {
        "en": [
            BotCommand("id", "Get chat ID")
        ],
        "ru": [
            BotCommand("id", "Узнать ID чата")
        ]
    }
    await bot.set_my_commands(
        commands=group_commands["ru"],
        scope=BotCommandScopeAllGroupChats(),
        language_code="ru"
    )
    await bot.set_my_commands(
        commands=group_commands["en"],
        scope=BotCommandScopeAllGroupChats(),
    )


def register(dp: Dispatcher):
    dp.register_message_handler(
        command_start, IsPrivate(), commands="start", state="*"
    )
    dp.register_message_handler(
        command_source, IsPrivate(), commands="source", state="*"
    )
    dp.register_message_handler(
        command_id, IsGroup(), commands="id", state="*"
    )
