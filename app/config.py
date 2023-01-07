from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    BOT_TOKEN: str
    GROUP_CHAT_ID: str
    CUSTOM_EMOJI_ID: str


def load_config():
    env = Env()
    env.read_env()

    return Config(
        BOT_TOKEN=env.str("BOT_TOKEN"),
        GROUP_CHAT_ID=env.str("GROUP_CHAT_ID"),
        CUSTOM_EMOJI_ID=env.str("CUSTOM_EMOJI_ID"),
    )
