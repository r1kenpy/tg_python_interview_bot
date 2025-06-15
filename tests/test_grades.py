from collections import namedtuple

import pytest

from app.utils.grades import get_grades


GRADE_FIELDS = ["id", "title", "question_id"]


def num_tee(fields, data):
    cls = namedtuple("Row", field_names=fields)
    return cls._make(data)


print(num_tee(GRADE_FIELDS, [2, "GRADE: 16", 1]))


@pytest.mark.parametrize(
    ["question_id", "excepted"],
    [
        [1, [num_tee(GRADE_FIELDS, [2, "GRADE: 16", 1])]],
        [
            2,
            [
                num_tee(GRADE_FIELDS, [3, "GRADE: 16", 1]),
                num_tee(GRADE_FIELDS, [4, "GRADE: 17", 1]),
                num_tee(GRADE_FIELDS, [5, "GRADE: 18", 1]),
            ],
        ],
        [3, []],
    ],
)
def test_get_grade_by_question_id(question_id, excepted):
    res = get_grades(question_id)
    assert res == excepted
