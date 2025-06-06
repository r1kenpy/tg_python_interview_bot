from db.db import get_connection
from db.sql import GET_GRADES_ID_AND_TITLE_BY_QUESTION_ID
from utils import get_logger

logger = get_logger()


def get_grades(question_id: int):
    with get_connection() as con:
        res = con.execute(
            GET_GRADES_ID_AND_TITLE_BY_QUESTION_ID, (question_id,)
        ).fetchall()
    return res
