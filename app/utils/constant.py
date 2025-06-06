import os
from pathlib import Path

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

PARSE_MODE = "Markdown"
NO_QUESTIONS = "Еще не добавили вопросы!"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TG_USER = int(os.getenv("TG_USER", "0"))
NEED_CREATE_DB = os.getenv("NEED_CREATE_DB", "")
DB_NAME = os.getenv("DB_NAME", "")

BASE_PATH = Path(__file__).parent.parent
TASK_PATH = BASE_PATH / "task"
TASK_PATH.mkdir(exist_ok=True)
PYTHON_TASK_PATH = TASK_PATH / "python"
PYTHON_TASK_PATH.mkdir(exist_ok=True)
PYTHON_QUESTIONS_PATH = PYTHON_TASK_PATH / "questions.json"
PYTHON_ANSWERS_PATH = PYTHON_TASK_PATH / "answers.json"
