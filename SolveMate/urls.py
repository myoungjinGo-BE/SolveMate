from django.urls import path, include
from rest_framework import routers
from SolveMate.api_docs.swagger import SwaggerSettings
from account.api.views import UserViewSet, KakaoOauthViewSet

# 기본 라우터
main_router = routers.DefaultRouter(trailing_slash=False)
main_router.register("users", UserViewSet)
swagger = SwaggerSettings()


api_url_patterns = [
    swagger.get_schema_path(),
    path("", include(main_router.urls)),
    path("oauth/kakao", KakaoOauthViewSet.as_view(), name="kakao-oauth-login"),
]

urlpatterns = [
    path("api/", include(api_url_patterns)),
]
