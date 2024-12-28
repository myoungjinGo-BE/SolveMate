from typing import Optional, Tuple
import requests

from SolveMate import settings
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class KakaoOauthService:
    KAKAO_GRANT_TYPE = "authorization_code"
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def authenticate_with_kakao(
        self, code: str
    ) -> Tuple[Optional[str], Optional[str], Optional[dict]]:
        """
        Kakao로부터 Access Token, Refresh Token 및 사용자 정보를 받아옵니다.
        """
        # Access Token 요청
        print(code, "d?")
        access_token = self._get_access_token(code)
        if not access_token:
            return None, None, None

        # 사용자 정보 요청
        user_info = self._get_user_info(access_token)
        if not user_info:
            return None, None, None

        kakao_id = user_info["id"]
        if self._is_user_exists(kakao_id):
            access_token, refresh_token = self._get_auth_token(kakao_id)
            return access_token, refresh_token, user_info

        return None, None, user_info

    def _get_access_token(self, code: str) -> Optional[str]:
        response = requests.post(
            self.KAKAO_TOKEN_URL,
            data={
                "grant_type": self.KAKAO_GRANT_TYPE,
                "client_id": settings.KAKAO_CLIENT_ID,
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": code,
                "client_secret": settings.KAKAO_CLIENT_SECRET,
            },
        )
        if response.status_code != 200:
            return None
        return response.json().get("access_token")

    def _get_user_info(self, access_token: str) -> Optional[dict]:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.KAKAO_USER_INFO_URL, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()

    def _is_user_exists(self, kakao_id: str) -> bool:
        return User.objects.filter(kakao_id=kakao_id).exists()

    def _get_auth_token(self, kakao_id: str) -> Tuple[str, str]:
        user = User.objects.get(kakao_id=kakao_id)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return str(access_token), str(refresh_token)
