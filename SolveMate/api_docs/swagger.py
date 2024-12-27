# Swagger 설정
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


class SwaggerSettings:
    def __init__(self):
        self.schema_view = get_schema_view(
            openapi.Info(
                title="SolveMate API",
                default_version="v1",
                description="API description",
                terms_of_service="https://solvemate.com/policies/terms/",
                contact=openapi.Contact(email="contact@solveMate.com"),
                license=openapi.License(name="BSD License"),
            ),
            public=True,
            permission_classes=[AllowAny],
        )

    def get_schema_path(self):
        return path(
            "swagger/",
            self.schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
