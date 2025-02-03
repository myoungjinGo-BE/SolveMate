from django.urls import path, include
from rest_framework import routers
from SolveMate.api_docs.swagger import SwaggerSettings
from account.views import UserViewSet, KakaoOauthViewSet
from challenge import views as challenge_views

# 기본 라우터
main_router = routers.DefaultRouter(trailing_slash=False)
main_router.register(r"users", UserViewSet)
main_router.register(r"problems", challenge_views.ProblemViewSet)
main_router.register(r"challenge-days", challenge_views.ChallengeDayViewSet)

swagger = SwaggerSettings()


api_url_patterns = [
    swagger.get_schema_path(),
    path("", include(main_router.urls)),
    path("oauth/kakao", KakaoOauthViewSet.as_view(), name="kakao-oauth-login"),
]

urlpatterns = [
    path("api/", include(api_url_patterns)),
]
