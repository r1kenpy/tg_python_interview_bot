import sqlite3
from collections import namedtuple
from contextlib import contextmanager
from sqlite3 import Connection

from utils import get_logger
from utils.constant import CATEGORIES, DB_NAME, GRADES
from db.sql import (
    ADD_ANSWERS_IN_TABLE,
    ADD_CATEGORY,
    ADD_GRADES_IN_TABLE,
    ADD_QUESTIONS_IN_TABLE,
    CREATE_TABLE_ANSWERS,
    CREATE_TABLE_CATEGORY,
    CREATE_TABLE_GRADES,
    CREATE_TABLE_QUESTIONS,
    GET_GRADE_ID_BY_TITLE,
    GET_QUESTION_ID_BY_TITLE,
)
from utils.parse_task import parse_file

logger = get_logger("init_db")


def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)


@contextmanager
def get_connection():
    try:
        con = sqlite3.connect(DB_NAME)
        con.row_factory = namedtuple_factory
        yield con
    finally:
        con.close()


class CreateDB:
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super().__new__(cls)
            cls.con = cls.__get_db_connection()
            cls.__initial_table()
        logger.info(cls.obj)
        return cls.obj

    @classmethod
    def __get_db_connection(cls) -> Connection:
        return sqlite3.connect(DB_NAME)

    @classmethod
    def __add_data_in_db(
        cls, answers_quesions: dict[str, list]
    ) -> list[tuple[str, int, int]]:
        data = []
        try:
            with cls.con:
                for key, value in answers_quesions.items():
                    logger.info(f"{key=}, {value=}")
                    question_id = cls.con.execute(
                        GET_QUESTION_ID_BY_TITLE, (key,)
                    ).fetchone()
                    logger.info(f"{question_id=}")
                    for answer in value:
                        logger.info(f"{answer=}")
                        grade_id = cls.con.execute(
                            GET_GRADE_ID_BY_TITLE, (answer["difficulty"],)
                        ).fetchone()
                        logger.info(f"{grade_id=}")

                        data.append((answer["content"], grade_id, question_id))

        except Exception as e:
            logger.exception(e)

        return data

    @classmethod
    def __create_table(cls) -> None:
        with cls.con:
            for sql in (
                CREATE_TABLE_ANSWERS,
                CREATE_TABLE_CATEGORY,
                CREATE_TABLE_GRADES,
                CREATE_TABLE_QUESTIONS,
            ):

                cls.con.executescript(sql)

    @classmethod
    def __add_data_in_table(cls, data, sql: str) -> None:
        with cls.con:
            try:
                cls.con.executemany(sql, data)
            except (sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
                logger.exception(e)

    @classmethod
    def __initial_table(cls) -> None:
        qestions, answers = parse_file()
        try:
            cls.__create_table()
            cls.__add_data_in_table(
                CATEGORIES,
                ADD_CATEGORY,
            )
            cls.__add_data_in_table(qestions, ADD_QUESTIONS_IN_TABLE)
            cls.__add_data_in_table(GRADES, ADD_GRADES_IN_TABLE)
            answers_for_db = cls.__add_data_in_db(
                answers,
            )
            cls.__add_data_in_table(answers_for_db, ADD_ANSWERS_IN_TABLE)
        except Exception as e:
            logger.exception(e)
        finally:
            cls.__close()

    @classmethod
    def __close(cls) -> None:
        cls.con.close()


if __name__ == "__main__":
    CreateDB()
