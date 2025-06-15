from db import cur
from db import get_connection
from db.sql import (
    GET_ADDITIONAL_BY_QUESTION_ID,
    GET_QUESTION_BY_ID,
    GET_RANDOM_QUESTIONS,
)
from utils import get_logger


logger = get_logger()


def get_question_text_by_id(question_id: int) -> str:
    # Возможно стоит отдавать голый результат.
    # А след шагом обрабатывать его преобразование в текст.
    # Так будет  чише. т.к. функция отвечает только за одно

    with get_connection() as con:
        res = con.execute(GET_QUESTION_BY_ID, (question_id,)).fetchone()
    return get_question_text(res)


def get_random_question():
    with get_connection() as c:
        return c.execute(GET_RANDOM_QUESTIONS).fetchone()


def get_question_id(question) -> int:
    return int(question.id)


def get_question_text(question) -> str:
    question_id = question.id
    question_text = question.text_question
    question_interview_count = (
        question.interview_count if question.interview_count is not None else 0
    )
    question_time = question.time_decision
    question_title = question.title.replace("_", "\\_")
    res = (
        f"Вопрос №{question_id}. {question_title}\n\nИспользований: "
        f"{question_interview_count} "
        f"| Время: {question_time}\n\n{question_text}"
    )
    logger.info(res)
    return res


def get_additional_by_question_id(question_id: int) -> str:
    text = ""
    with get_connection() as con:
        res = con.execute(
            GET_ADDITIONAL_BY_QUESTION_ID, (question_id,)
        ).fetchone()

    logger.info(res)

    additional = res.additional
    if additional:
        text = (
            f"Дополнительные вопросы на вопрос №{question_id}.\n\n{additional}"
        )

    return text
