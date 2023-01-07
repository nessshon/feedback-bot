from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Unauthorized
from aiogram.utils import executor


def init():
    from . import logging
    logging.setup()

    from .config import Config, load_config
    config: Config = load_config()

    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    bot["config"] = config

    try:
        from . import main

        executor.start_polling(
            dispatcher=dp,
            skip_updates=False,
            reset_webhook=True,
            on_startup=main.on_startup,
            on_shutdown=main.on_shutdown
        )

    except Unauthorized:
        logging.logger.error("Invalid bot token!")

    except Exception as e:
        logging.logger.error(e)


if __name__ == "__main__":
    init()
