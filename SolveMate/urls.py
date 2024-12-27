from django.urls import path, include
from rest_framework import routers
from SolveMate.api_docs.swagger import SwaggerSettings
from account.api.views import UserViewSet

# 기본 라우터
main_router = routers.DefaultRouter(trailing_slash=False)
main_router.register("users", UserViewSet)
swagger = SwaggerSettings()

urlpatterns = [
    swagger.get_schema_path(),
    path("api/", include(main_router.urls)),
]
