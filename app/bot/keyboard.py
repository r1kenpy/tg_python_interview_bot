from telebot.types import InlineKeyboardButton as Button
from telebot.types import InlineKeyboardMarkup as Markup

from utils import get_logger
from bot.factory import (
    back_questions_factory,
    grades_factory,
    question_factory,
)

logger = get_logger()


class InlineKeyboardButton(Button):
    def __repr__(self):
        return self.text


class InlineKeyboardMarkup(Markup):
    def __repr__(self):
        return f"{self.keyboard}"


def questions_keyboard(grades) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text=grade.title,
                    callback_data=grades_factory.new(
                        grade_id=grade.id, question_id=grade.question_id
                    ),
                )
            ]
            for grade in grades
        ]
    )

    k.add(
        InlineKeyboardButton(text="Следующий вопрос ➡", callback_data="next")
    )
    logger.info(k)
    return k


def back_keyboard(question_id):
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data=back_questions_factory.new(
                        question_id=question_id
                    ),
                )
            ]
        ]
    )


def add_additional_to_keyboard(
    question_id: int, keyboard: InlineKeyboardMarkup
) -> InlineKeyboardMarkup:
    logger.info(keyboard)
    keyboard.add(
        InlineKeyboardButton(
            text="Дополнительные вопросы",
            callback_data=question_factory.new(question_id),
        )
    )
    return keyboard
