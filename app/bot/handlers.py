import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import Message, User
from aiogram.utils.exceptions import BadRequest, BotBlocked

from app.config import Config
from app.database.models.users import UserModel

from .texts import Text
from .filters import IsPrivate, IsGroup
from .misc import rate_limit, delete_message


async def create_forum_topic(bot: Bot, user: User, config: Config) -> int:
    forum_topic = await bot.create_forum_topic(
        chat_id=config.GROUP_CHAT_ID, name=user.first_name,
        icon_custom_emoji_id=config.CUSTOM_EMOJI_ID
    )
    message_thread_id = forum_topic.message_thread_id

    await UserModel.update(
        user_id=user.id,
        message_thread_id=message_thread_id
    )

    return message_thread_id


@rate_limit(1)
async def private_chat_message_handler(message: Message):
    user = User.get_current()
    config: Config = message.bot.get("config")
    message_thread_id = await UserModel.get_message_thread_id(user.id)

    if message_thread_id is None:
        message_thread_id = await create_forum_topic(
            bot=message.bot, user=user, config=config
        )

    if not await UserModel.is_forum_topic_closed(message_thread_id):
        text = Text().get_message("MESSAGE_SENT")

        try:
            await message.forward(
                chat_id=config.GROUP_CHAT_ID,
                message_thread_id=message_thread_id
            )

        except BadRequest as error:
            if error.check("Message thread not found"):
                message_thread_id = await create_forum_topic(
                    bot=message.bot, user=user, config=config
                )

                await message.forward(
                    chat_id=config.GROUP_CHAT_ID,
                    message_thread_id=message_thread_id
                )
            else:
                text = Text().get_message("UNKNOWN_ERROR")

        msg = await message.reply(text)
        await asyncio.sleep(3)
        await delete_message(msg)


@rate_limit(0.5)
async def group_chat_message_handler(message: Message):
    if message.reply_to_message and message.reply_to_message.is_forward():
        try:
            user_id = await UserModel.get_user_id(message.message_thread_id)
            await message.copy_to(chat_id=user_id)

        except BotBlocked:
            text = Text().get_message("BOT_BLOCKED")
            await message.answer(text)

        except Exception as error:
            text = Text().get_message("UNKNOWN_ERROR")
            await message.reply(text)
            logging.error(error)

    if message.forum_topic_closed or message.forum_topic_reopened:
        user_id = await UserModel.get_user_id(message.message_thread_id)
        forum_topic_closed = True if message.forum_topic_closed else False

        await UserModel.update(
            user_id=user_id,
            forum_topic_closed=forum_topic_closed
        )


def register(dp: Dispatcher):
    dp.register_message_handler(
        private_chat_message_handler, IsPrivate(),
        content_types="any"
    )
    dp.register_message_handler(
        group_chat_message_handler, IsGroup(),
        content_types="any"
    )
