import pytest

from rest_framework.test import APIClient
from freezegun import freeze_time


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def frozen_time():
    with freeze_time("2025-02-04 00:00:00"):
        yield


@pytest.mark.django_db
class TestProblemSearch:
    """
    문제 검색 API 테스트
    """

    def test_문제_조회_테스트_제목(self, api_client, 예시_문제_생성):
        res = api_client.get("/api/problems/search", {"query": "예시"})
        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [
                {
                    "id": 1,
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1000",
                    "created_at": "2025-02-04T09:00:00+09:00",
                },
                {
                    "id": 2,
                    "title": "예시_문제_2",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1001",
                    "created_at": "2025-02-04T09:00:00+09:00",
                },
                {
                    "id": 3,
                    "title": "예시_문제_3",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1002",
                    "created_at": "2025-02-04T09:00:00+09:00",
                },
            ],
        }

    def test_문제_조회_테스트_문제_번호(self, api_client, 예시_문제_생성):
        res = api_client.get("/api/problems/search", {"query": "1000"})
        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [
                {
                    "id": 1,
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1000",
                    "created_at": "2025-02-04T09:00:00+09:00",
                }
            ],
        }

    def test_문제_조회_테스트_검색어_없음(self, api_client, 예시_문제_생성):
        res = api_client.get("/api/problems/search", {"query": ""})
        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [],
        }


@pytest.mark.django_db
class TestChallengeDay:
    def test_챌린지_문제_생성_테스트_no_problems(self, api_client, challenge_user):
        """
        문제가 생성 되어있지 않은 경우 챌린지 문제를 생성하는 테스트
        """
        api_client.force_authenticate(user=challenge_user)

        res = api_client.post(
            "/api/challenge-days",
            {
                "date": "2025-02-04",
                "problem": {
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "link": "https://www.acmicpc.net/problem/1000",
                },
            },
            format="json",
        )

        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": {
                "date": "2025-02-04",
                "problem": {
                    "id": 1,
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1000",
                    "created_at": "2025-02-04T09:00:00+09:00",
                },
                "group": 1,
                "author": 1,
            },
        }

    def test_챌린지_문제_생성_테스트(self, api_client, challenge_user, 예시_문제_생성):
        """
        문제가 이미 생성 되어있는 경우 챌린지 문제를 생성하는 테스트
        """
        api_client.force_authenticate(user=challenge_user)

        res = api_client.post(
            "/api/challenge-days",
            {
                "date": "2025-02-04",
                "problem": {
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "link": "https://www.acmicpc.net/problem/1000",
                },
            },
            format="json",
        )

        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": {
                "date": "2025-02-04",
                "problem": {
                    "id": 1,
                    "title": "예시_문제_1",
                    "platform": "BAEKJOON",
                    "platform_display": "백준",
                    "link": "https://www.acmicpc.net/problem/1000",
                    "created_at": "2025-02-04T09:00:00+09:00",
                },
                "group": 1,
                "author": 1,
            },
        }

    def test_챌린지_미존재_문제_목록_조회_테스트(
        self, api_client, challenge_user, 예시_문제_생성
    ):
        """ "
        챌린지데이 문제가 없는 경우
        """

        api_client.force_authenticate(user=challenge_user)

        res = api_client.get("/api/challenge-days")

        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [],
        }

    def test_챌린지_문제_목록_조회_테스트(
        self, api_client, challenge_user, 예시_챌린지_문제_생성
    ):
        """
        챌린지데이 문제가 있는 경우
        """
        api_client.force_authenticate(user=challenge_user)

        res = api_client.get("/api/challenge-days")

        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [
                {
                    "date": "2025-02-01",
                    "problem": {
                        "id": 1,
                        "title": "예시_문제_1",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1000",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-02",
                    "problem": {
                        "id": 2,
                        "title": "예시_문제_2",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1001",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-03",
                    "problem": {
                        "id": 3,
                        "title": "예시_문제_3",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1002",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-04",
                    "problem": {
                        "id": 1,
                        "title": "예시_문제_1",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1000",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-05",
                    "problem": {
                        "id": 2,
                        "title": "예시_문제_2",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1001",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-06",
                    "problem": {
                        "id": 3,
                        "title": "예시_문제_3",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1002",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-07",
                    "problem": {
                        "id": 1,
                        "title": "예시_문제_1",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1000",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
            ],
        }

    def test_챌린지_문제_목록_조회_테스트_다른_날짜(
        self, api_client, challenge_user, 예시_챌린지_문제_생성
    ):
        """
        기준 날짜인 2월4일이 아닌 2월 1일을 기준으로 조회하는 경우
        2월 1일 ~ 2월 4일까지의 데이터만 가져와야 한다.
        """

        api_client.force_authenticate(user=challenge_user)

        res = api_client.get("/api/challenge-days", {"date": "2025-02-01"})

        assert res.json() == {
            "status": "success",
            "message": "Operation succeeded",
            "data": [
                {
                    "date": "2025-02-01",
                    "problem": {
                        "id": 1,
                        "title": "예시_문제_1",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1000",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-02",
                    "problem": {
                        "id": 2,
                        "title": "예시_문제_2",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1001",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-03",
                    "problem": {
                        "id": 3,
                        "title": "예시_문제_3",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1002",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
                {
                    "date": "2025-02-04",
                    "problem": {
                        "id": 1,
                        "title": "예시_문제_1",
                        "platform": "BAEKJOON",
                        "platform_display": "백준",
                        "link": "https://www.acmicpc.net/problem/1000",
                        "created_at": "2025-02-04T09:00:00+09:00",
                    },
                    "group": 1,
                    "author": 1,
                },
            ],
        }
