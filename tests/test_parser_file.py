from pathlib import Path

import pytest

from app.utils.parse_file import parse_file


BASE_PATH = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    ["file_name", "expected"],
    [
        (
            "many_questions_for_test.json",
            [
                [
                    "Test Title questions",
                    "test additional",
                    1,
                    10,
                    "text question TEST",
                    10,
                ],
                [
                    "Test Title 2",
                    "test additional 2",
                    2,
                    20,
                    "2 text question TEST ",
                    0,
                ],
            ],
        ),
        (
            "one_question_for_test.json",
            [
                [
                    "Test Title questions",
                    "test additional",
                    1,
                    10,
                    "text question TEST",
                    10,
                ]
            ],
        ),
        (
            "many_answers_for_test.json",
            [
                ["Test answer content", 2, 1],
                ["Test answer 2 content", 3, 2],
            ],
        ),
        ("one_answer_for_test.json", [["Test answer content", 2, 1]]),
        ("None_in_answer_for_test.json", [[None, None, None]]),
    ],
)
def test_parse_file(file_name, expected):
    assert parse_file(BASE_PATH / file_name) == expected
