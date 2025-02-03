import pytest

from challenge.models import Problem


@pytest.fixture()
def 예시_문제_생성():
    problems = [
        Problem(
            title="예시_문제_1",
            problem_id="1000",
            platform="BAEKJOON",
            link="https://www.acmicpc.net/problem/1000",
        ),
        Problem(
            title="예시_문제_2",
            problem_id="1005",
            platform="BAEKJOON",
            link="https://www.acmicpc.net/problem/1001",
        ),
        Problem(
            title="예시_문제_3",
            problem_id="2000",
            platform="BAEKJOON",
            link="https://www.acmicpc.net/problem/1002",
        ),
    ]

    Problem.objects.bulk_create(problems)
    x = Problem.objects.all()
