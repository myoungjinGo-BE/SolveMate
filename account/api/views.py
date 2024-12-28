from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers import UserSerializer
from account.models import User
from account.services.kako_oauth_service import KakaoOauthService
from account.services.token_service import TokenService


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-up",
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = TokenService.generate_tokens_for_user(user)
        response_data = serializer.data
        response_data.update(tokens)

        return Response(response_data, status=status.HTTP_201_CREATED)


class KakaoOauthViewSet(APIView):
    FRONT_END_ENDPOINT = "https://your-frontend-endpoint.com"

    def __init__(self):
        super().__init__()

        self.kakao_service = KakaoOauthService()

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Missing code parameter"}, status=status.HTTP_400_BAD_REQUEST
            )

        # KakaoOauthService에서 인증 및 사용자 정보 가져오기
        access_token, refresh_token, user_info = (
            self.kakao_service.authenticate_with_kakao(code)
        )

        if not user_info:
            return Response(
                {"error": "Failed to authenticate with Kakao"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if access_token and refresh_token:
            # 이미 가입된 사용자
            return redirect(
                f"{self.FRONT_END_ENDPOINT}/login?access_token={access_token}&refresh_token={refresh_token}"
            )

        # 신규 사용자 회원가입 경로로 리다이렉트
        return redirect(
            f'{self.FRONT_END_ENDPOINT}/signup?kakao_id={user_info["id"]}'
            f'&username={user_info["properties"]["nickname"]}'
            f'&profile_image={user_info["properties"]["profile_image"]}'
        )
