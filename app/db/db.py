import sqlite3
from collections import namedtuple
from contextlib import contextmanager
from typing import Any

from utils import get_logger
from utils.constant import (
    CATEGORIES,
    DB_NAME,
    GRADES,
    NEED_CREATE_DB,
    PYTHON_ANSWERS_PATH,
    PYTHON_QUESTIONS_PATH,
)
from utils.parse_file import parse_file

from .sql import (
    ADD_ANSWERS_IN_TABLE,
    ADD_CATEGORY,
    ADD_GRADES_IN_TABLE,
    ADD_QUESTIONS_IN_TABLE,
    CREATE_TABLE_ANSWERS,
    CREATE_TABLE_CATEGORY,
    CREATE_TABLE_GRADES,
    CREATE_TABLE_QUESTIONS,
)

logger = get_logger("init_db")


def __namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)


@contextmanager
def get_connection(db_name: str = DB_NAME):
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = __namedtuple_factory
        yield con
    finally:
        con.close()


class WorkingWithDB:
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super().__new__(cls, *args, **kwargs)
            if isinstance(NEED_CREATE_DB, str) and NEED_CREATE_DB == "True":
                logger.info("Инициализация DB")
                cls.__initial_table()
        logger.info(cls.obj)
        return cls.obj

    @staticmethod
    def create_table(sql_scripts: list[str] | tuple[str, ...]) -> None:
        for sql_script in sql_scripts:
            if "CREATE TABLE IF NOT EXISTS" not in sql_script:
                raise

        with get_connection() as con:
            for sql in sql_scripts:
                con.executescript(sql)

    @staticmethod
    def add_many_data_in_table(
        sql_query: str,
        data: list[list[Any]] | tuple[tuple[Any]] | tuple[tuple[Any, ...]],
    ) -> None:
        with get_connection() as con:
            try:
                con.executemany(sql_query, data)

                con.commit()
            except (sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
                logger.exception(e)

    @staticmethod
    def get_data_from_db(sql_query: str, data: Any = None):
        with get_connection() as con:
            try:
                if data is None:
                    return con.executescript(sql_query).fetchone()
                return con.execute(sql_query, data).fetchone()
            except (sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
                logger.exception(e)

    @classmethod
    def __initial_table(cls) -> None:
        try:
            cls.create_table(
                (
                    CREATE_TABLE_ANSWERS,
                    CREATE_TABLE_CATEGORY,
                    CREATE_TABLE_GRADES,
                    CREATE_TABLE_QUESTIONS,
                )
            )
            logger.info("Таблицы созданы")

            qestions = parse_file(PYTHON_QUESTIONS_PATH)
            logger.info(f"{qestions=}"[:100])

            answers = parse_file(PYTHON_ANSWERS_PATH)
            logger.info(f"{answers=}"[:100])

            cls.add_many_data_in_table(ADD_CATEGORY, CATEGORIES)
            logger.info(f"Добавлены категории: {CATEGORIES=}"[:100])

            cls.add_many_data_in_table(ADD_QUESTIONS_IN_TABLE, qestions)
            logger.info(f"Добавлены вопросы: {qestions=}"[:100])

            cls.add_many_data_in_table(ADD_GRADES_IN_TABLE, GRADES)
            logger.info(f"Добавлены грейды: {GRADES=}"[:100])

            cls.add_many_data_in_table(ADD_ANSWERS_IN_TABLE, answers)
            logger.info(f"Добавлены ответы на вопросы: {answers=}"[:100])

        except Exception as e:
            logger.exception(e)
