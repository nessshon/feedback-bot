from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatType


class IsGroup(BoundFilter):

    async def check(self, message: Message) -> bool:
        return message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
