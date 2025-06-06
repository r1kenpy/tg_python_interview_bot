import sqlite3
from collections import namedtuple
from contextlib import contextmanager
from sqlite3 import Connection

from db.sql import (
    ADD_ANSWERS_IN_TABLE,
    ADD_CATEGORY,
    ADD_GRADES_IN_TABLE,
    ADD_QUESTIONS_IN_TABLE,
    CREATE_TABLE_ANSWERS,
    CREATE_TABLE_CATEGORY,
    CREATE_TABLE_GRADES,
    CREATE_TABLE_QUESTIONS,
)
from utils import get_logger
from utils.constant import (
    CATEGORIES,
    DB_NAME,
    GRADES,
    PYTHON_ANSWERS_PATH,
    PYTHON_QUESTIONS_PATH,
)
from utils.parse_file import parse_file

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
    def __add_data_in_table(cls, data: list[list], sql: str) -> None:
        with cls.con:
            try:
                cls.con.executemany(sql, data)
            except (sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
                logger.exception(e)

    @classmethod
    def __initial_table(cls) -> None:

        try:
            qestions = parse_file(PYTHON_QUESTIONS_PATH)
            logger.info(f"{qestions=}"[:100])
            answers = parse_file(PYTHON_ANSWERS_PATH)
            logger.info(f"{answers=}"[:100])
            cls.__create_table()
            logger.info("Таблицы созданы")
            cls.__add_data_in_table(
                CATEGORIES,
                ADD_CATEGORY,
            )
            logger.info(f"Добавлены категории: {CATEGORIES=}"[:100])
            cls.__add_data_in_table(qestions, ADD_QUESTIONS_IN_TABLE)
            logger.info(f"Добавлены вопросы: {qestions=}"[:100])
            cls.__add_data_in_table(GRADES, ADD_GRADES_IN_TABLE)
            logger.info(f"Добавлены грейды: {GRADES=}"[:100])
            cls.__add_data_in_table(answers, ADD_ANSWERS_IN_TABLE)
            logger.info(f"Добавлены ответы на вопросы: {answers=}"[:100])
        except Exception as e:
            logger.exception(e)
        finally:
            cls.__close()

    @classmethod
    def __close(cls) -> None:
        cls.con.close()


if __name__ == "__main__":
    CreateDB()
