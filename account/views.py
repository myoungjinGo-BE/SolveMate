import os

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import redirect


from account.serializers import UserSerializer
from account.models import User
from account.services.kako_oauth_service import KakaoOauthService
from account.services.user.services import UserService


class UserViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    user_service = UserService()

    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-up",
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        res_data = self.user_service.sign_up_user(request.data)
        return Response(res_data, status=status.HTTP_201_CREATED)


class KakaoOauthViewSet(APIView):
    def __init__(self):
        super().__init__()
        self.kakao_service = KakaoOauthService()

    def redirect_with_tokens(self, access_token: str, refresh_token: str):
        """
        이미 가입된 사용자를 로그인 페이지로 리다이렉트합니다.
        """
        return redirect(
            f"{os.getenv("FRONT_END_ENDPOINT")}/auth/login"
            f"?access_token={access_token}&refresh_token={refresh_token}"
        )

    def redirect_to_signup(self, kakao_id: str, username: str, profile_image: str):
        """
        신규 사용자를 회원가입 페이지로 리다이렉트합니다.
        """
        return redirect(
            f"{os.getenv("FRONT_END_ENDPOINT")}/auth/signup"
            f"?kakao_id={kakao_id}&username={username}&profile_image={profile_image}"
        )

    @swagger_auto_schema(
        operation_summary="카카오 인증 엔드포인트",
        operation_description="카카오 인증 후 리다이렉트 처리",
        operation_id="kakao_oauth_login",
        tags=["oauth"],
    )
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
            return self.redirect_with_tokens(access_token, refresh_token)

        # 신규 사용자 회원가입 경로로 리다이렉트
        return self.redirect_to_signup(
            kakao_id=user_info["id"],
            username=user_info["properties"]["nickname"],
            profile_image=user_info["properties"]["profile_image"],
        )
