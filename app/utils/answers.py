from db.db import get_connection
from db.sql import GET_ANSWERS_BY_QUESTION_AND_GRADE_ID
from utils import get_logger

logger = get_logger()


def get_answer(question_id, grade_id) -> str:
    text = ""
    with get_connection() as con:
        answer = con.execute(
            GET_ANSWERS_BY_QUESTION_AND_GRADE_ID, (question_id, grade_id)
        ).fetchone()
    logger.info(answer)
    if answer.a_id:
        grade = answer.grade.lower()
        text = f"Вопрос №{question_id} | {grade}\n\n{answer.content}"

    logger.info(text)
    return text
