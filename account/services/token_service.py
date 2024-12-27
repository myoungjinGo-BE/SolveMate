from rest_framework_simplejwt.tokens import RefreshToken


class TokenService:
    @staticmethod
    def generate_tokens_for_user(user):
        """
        주어진 사용자를 기반으로 액세스 토큰과 리프레시 토큰 생성
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
