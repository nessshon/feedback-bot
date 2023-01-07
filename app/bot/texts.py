from aiogram.types import User


class Text:
    messages = {
        "en": {
            "START": (
                "<b>Hello, {}!</b>\n\n"
                "This is <b>Ness Projects</b> Feedback Bot.\n\n"
                "Write your question, and we will answer you as soon as possible."
            ),
            "SOURCE": (
                "https://github.com/nessshon/feedback-bot"
            ),
            "MESSAGE_SENT": (
                "<b>Message sent!</b> Expect a response."
            ),
            "BOT_BLOCKED": (
                "<b>Message not sent!</b>"
                "Bot was blocked by the user."
            ),
            "UNKNOWN_ERROR": (
                "<b>An unexpected error has occurred!</b>"
            )
        },
        "ru": {
            "START": (
                "<b>Привет, {}!</b>\n\n"
                "Это бот обратной связи <b>Ness Projects</b>.\n\n"
                "<b>Напишите ваш вопрос и мы ответим вам в ближайшее время.</b>"
            ),
            "SOURCE": (
                "https://github.com/nessshon/feedback-bot"
            ),
            "MESSAGE_SENT": (
                "<b>Сообщение отправлено!</b> Ожидайте ответа."
            ),
            "BOT_BLOCKED": (
                "<b>Сообщение не отправлено!</b>"
                "Бот был заблокирован пользователем."
            ),
            "UNKNOWN_ERROR": (
                "<b>Произошла непредвиденная ошибка!</b>"
            )
        },
    }

    def __init__(self):
        language_code = User.get_current().language_code
        self.language_code = language_code if language_code == "ru" else "en"

    def get_message(self, key: str) -> str:
        return self.messages[self.language_code][key]
