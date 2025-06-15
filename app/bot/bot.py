import telebot
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import CallbackQuery

from db import WorkingWithDB
from .factory import back_questions_factory, grades_factory, question_factory
from .keyboard import (
    add_additional_to_keyboard,
    back_keyboard,
    questions_keyboard,
)
from utils import get_logger
from utils.answers import get_answer
from utils.constant import BOT_TOKEN, NO_QUESTIONS, PARSE_MODE, TG_USER
from utils.grades import get_grades
from utils.questions import (
    get_additional_by_question_id,
    get_question_id,
    get_question_text_by_id,
    get_random_question,
)

bot = telebot.TeleBot(BOT_TOKEN)
logger = get_logger()


class GradesCallbackFilter(AdvancedCustomFilter):
    key = "config"

    def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


bot.add_custom_filter(GradesCallbackFilter())


def return_all(question_db):
    question_id = get_question_id(question_db)
    question_text = get_question_text_by_id(question_id)
    logger.info((question_db, question_id, question_text))
    grades = get_grades(question_id)
    return (question_text, grades)


@bot.message_handler(
    commands=["start"], func=lambda m: m.from_user.id == TG_USER
)
def start_message(message):
    question_in_db = get_random_question()
    keyboard = None
    logger.info(f"{question_in_db=}")
    try:
        question_id = question_in_db.id
    except AttributeError as e:
        question_id = None
        logger.exception(e)

    if question_id is not None:
        question_text = get_question_text_by_id(question_id)
        grades = get_grades(question_id)
        keyboard = questions_keyboard(grades)
    else:
        question_text = NO_QUESTIONS
    logger.info(f"{question_text=}, {keyboard=}")
    bot.send_message(
        chat_id=message.chat.id,
        text=question_text,
        parse_mode=PARSE_MODE,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda c: c.data == "next")
def next_callback(call: CallbackQuery):
    question_in_db = get_random_question()
    keyboard = None
    logger.info(f"{question_in_db=}")
    if question_in_db is not None:
        question_id = get_question_id(question_in_db)
        question_additional = get_additional_by_question_id(question_id)
        question_text, grades = return_all(question_in_db)

        keyboard = questions_keyboard(grades)
        if question_additional:
            keyboard = add_additional_to_keyboard(question_id, keyboard)
    else:
        question_text = NO_QUESTIONS
    logger.info(f"{question_text=}, {keyboard=}")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=question_text,
        reply_markup=keyboard,
        parse_mode=PARSE_MODE,
    )


@bot.callback_query_handler(func=None, config=grades_factory.filter())
def answers_callback(call: CallbackQuery):
    logger.info(call.data)

    callback_data: dict = grades_factory.parse(callback_data=call.data)
    grade_id = callback_data.get("grade_id", "")
    question_id = callback_data.get("question_id", "")
    text = get_answer(question_id, grade_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=back_keyboard(question_id),
        parse_mode=PARSE_MODE,
    )


@bot.callback_query_handler(func=lambda c: "back" in c.data)
def back_callback(call: CallbackQuery):
    logger.info(call.data)
    callback_data = back_questions_factory.parse(callback_data=call.data)
    question_id = callback_data.get("question_id", "")

    if question_id.isdigit():
        question_id = int(question_id)

    question = get_question_text_by_id(question_id)
    grades = get_grades(question_id)
    additional = get_additional_by_question_id(question_id)
    keyboard = questions_keyboard(grades)

    if additional:
        keyboard = add_additional_to_keyboard(question_id, keyboard)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=question,
        reply_markup=keyboard,
        parse_mode=PARSE_MODE,
    )


@bot.callback_query_handler(func=lambda c: "additional" in c.data)
def additional_callback(call: CallbackData):
    logger.info(call.data)
    question_id = question_factory.parse(callback_data=call.data).get(
        "question_id", ""
    )
    if question_id.isdigit():
        question_id = int(question_id)
    text = get_additional_by_question_id(question_id)
    logger.info(text)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=back_keyboard(question_id),
        parse_mode=PARSE_MODE,
    )
