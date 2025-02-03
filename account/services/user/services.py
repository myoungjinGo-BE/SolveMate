from rest_framework.exceptions import ValidationError

from account.serializers import UserSerializer
from account.services.token_service import TokenService
from challenge.services.group.services import GroupService


class UserService:
    @staticmethod
    def sign_up_user(user_data):
        """
        사용자 회원가입 처리 및 기본 그룹 추가
        """
        # 유저 데이터 직렬화 및 저장
        serializer = UserSerializer(data=user_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        user = serializer.save()

        # 기본 그룹에 추가
        group_service = GroupService()
        group_service.join_default_group(user)

        # 토큰 생성
        tokens = TokenService.generate_tokens_for_user(user)

        # 반환 데이터 구성
        response_data = serializer.data
        response_data.update(tokens)
        return response_data
