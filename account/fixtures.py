import pytest

from account.models import User
from challenge.models import ChallengeGroup


@pytest.fixture()
def 카카오_가입_유저_생성():
    return User.objects.create(
        username="카카오_유저",
        nickname="카카오_닉네임",
        profile_picture="http://kakao.com",
        kakao_id="kakao",
    )


@pytest.fixture()
def 기본_챌린지_그룹_생성():
    return ChallengeGroup.objects.create(name="기본_그룹")
