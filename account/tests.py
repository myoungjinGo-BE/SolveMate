from rest_framework.test import APIClient

from account.services.token_service import TokenService
from account.conftest import *
from challenge.models import GroupMembership
from challenge.services.group.services import GroupService


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestTokenService:
    def test_토큰_생성_테스트(self, 카카오_가입_유저_생성):
        user = 카카오_가입_유저_생성
        tokens = TokenService.generate_tokens_for_user(user)

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["access_token"] != tokens["refresh_token"]


@pytest.mark.django_db
class TestUserViewSet:
    def test_회원가입_테스트(self, api_client):
        # given
        signup_data = {
            "kakao_id": "kakao",
            "username": "test",
            "nickname": "test",
            "profile_picture": "http://test.com",
        }

        # when
        res = api_client.post("/api/users/sign-up", signup_data)

        # then
        result = res.json()
        assert res.status_code == 201
        assert "access_token" in result
        assert "refresh_token" in result

        # 유저가 그룹에 생성 되었는지 확인
        assert User.objects.filter(username="test").exists()
        assert ChallengeGroup.objects.filter(
            name=GroupService.DEFAULT_GROUP_NAME
        ).exists()
        assert GroupMembership.objects.filter(user__username="test").exists()
