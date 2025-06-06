from telebot.callback_data import CallbackData

grades_factory = CallbackData(
    "grade_id", "question_id", prefix="grades_and_questions"
)

back_questions_factory = CallbackData("question_id", prefix="back_question")

question_factory = CallbackData("question_id", prefix="additional_question")
