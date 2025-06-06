import os

from dotenv import load_dotenv

load_dotenv(".env")


GRADES = (
    ("UNKNOWN",),
    ("GRADE_16",),
    ("GRADE_17",),
    ("GRADE_18",),
    ("GRADE_19",),
    ("GRADE_20",),
    ("GRADE_SCREENING",),
)

CATEGORIES = (("Python",),)


MAX_ROW_WIDTH = 2
PARSE_MODE = "Markdown"
NO_QUESTIONS = "Еще не добавили вопросы!"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TG_USER = int(os.getenv("TG_USER", "0"))
NEED_CREATE_DB = os.getenv("NEED_CREATE_DB", "")
DB_NAME = os.getenv("DB_NAME", "")
