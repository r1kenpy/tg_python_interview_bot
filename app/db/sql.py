# ---------------------------------------
# Получение данныех из таблицы
# ---------------------------------------
GET_RANDOM_QUESTIONS = """
    SELECT *
    FROM questions
    ORDER BY RANDOM();"""

GET_GRADE_ID_BY_TITLE = """
    SELECT id as id
    FROM grades
    WHERE title=?;"""

GET_QUESTION_ID_BY_TITLE = """
    SELECT id as id
    FROM questions
    WHERE title=?;
"""
GET_QUESTION_BY_ID = """
    SELECT *
    FROM questions
    WHERE id=?;
"""
GET_ANSWERS_BY_QUESTION_AND_GRADE_ID = """
    SELECT a.id as a_id, g.id as g_id, a.content, g.title as grade
    FROM answers a
    JOIN grades g on g.id=a.grade_id
    WHERE a.question_id=? and a.grade_id=?;
"""

GET_ALL_GRADES = """SELECT * FROM grades;"""

GET_GRADES_ID_AND_TITLE_BY_QUESTION_ID = """
    SELECT g.id as id, g.title as title, a.question_id as question_id
    FROM grades g
    JOIN answers a on a.grade_id=g.id
    where a.question_id=?;
"""

GET_ADDITIONAL_BY_QUESTION_ID = """
    SELECT additional
    FROM questions
    WHERE id=?;
"""

# ---------------------------------------
# Добавление данных в таблицу таблиц начальными данными
# ---------------------------------------
ADD_ANSWERS_IN_TABLE = """
    INSERT OR IGNORE INTO answers(content, grade_id, question_id)
    VALUES (?,?,?);
"""

ADD_GRADES_IN_TABLE = """
    INSERT OR IGNORE INTO grades(title) VALUES(?);
"""

ADD_QUESTIONS_IN_TABLE = """
    INSERT OR IGNORE INTO questions(
        title,
        additional,
        category_id,
        interview_count,
        text_question,
        time_decision)
    VALUES (?,?,?,?,?,?);
    """

ADD_CATEGORY = "INSERT OR IGNORE INTO categories(title) VALUES (?);"


# ---------------------------------------
# Создание таблиц
# ---------------------------------------
CREATE_TABLE_GRADES = """
    CREATE TABLE IF NOT EXISTS grades(
        id INTEGER PRIMARY KEY,
        title VARCHAR(50) UNIQUE NOT NULL
    );"""

CREATE_TABLE_QUESTIONS = """
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY,
        title VARCHAR(255) UNIQUE NOT NULL,
        additional TEXT,
        category_id INTEGER NOT NULL ,
        interview_count int CHECK(interview_count >= 0) DEFAULT 0,
        text_question TEXT NOT NULL,
        time_decision INTEGER  DEFAULT 10 CHECK(time_decision >= 1),
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );"""
# На вопрос должне быть только 1 ответ с одним грейдом. Нельзя сделать несколько ответов с одинаковым грейдом.
CREATE_TABLE_ANSWERS = """
    CREATE TABLE IF NOT EXISTS answers(
        id INTEGER PRIMARY KEY,
        content TEXT UNIQUE NOT NULL,
        grade_id INTEGER NOT NULL DEFAULT 1, 
        question_id INTEGER NOT NULL CHECK(question_id >= 1),
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
        FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE SET DEFAULT);"""


CREATE_TABLE_CATEGORY = """
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY,
        title VARCHAR(255) UNIQUE NOT NULL
    );"""
