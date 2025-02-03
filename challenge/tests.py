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
