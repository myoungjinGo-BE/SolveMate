import pytest

from account.models import User
from challenge.models import Problem, ChallengeDay
from challenge.services.group.services import GroupService


@pytest.fixture()
def challenge_user():
    challenge_user = User.objects.create(
        username="챌린지_유저",
        nickname="챌린지_닉네임",
        profile_picture="http://solve-mate.com",
        kakao_id="kakao",
    )
    group_service = GroupService()
    group_service.join_default_group(challenge_user)

    return challenge_user


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
    return problems


@pytest.fixture()
def 예시_챌린지_문제_생성(challenge_user, 예시_문제_생성):
    problems = 예시_문제_생성

    # 2025년 2월 4일 앞뒤로 3일 총 7일 생성
    # 생성한 유저(author) 및 그룹(group), date 필요

    ChallengeDay.objects.bulk_create(
        [
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-01",
                problem=problems[0],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-02",
                problem=problems[1],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-03",
                problem=problems[2],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-04",
                problem=problems[0],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-05",
                problem=problems[1],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-06",
                problem=problems[2],
            ),
            ChallengeDay(
                author=challenge_user,
                group=challenge_user.default_group,
                date="2025-02-07",
                problem=problems[0],
            ),
        ]
    )
