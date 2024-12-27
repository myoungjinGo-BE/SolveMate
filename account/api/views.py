from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.api.serializers import SignUpSerializer
from account.models import User
from account.services.token_service import TokenService


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-up",
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)  # 직접 지정
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = TokenService.generate_tokens_for_user(user)
        response_data = serializer.data
        response_data.update(tokens)

        return Response(response_data, status=status.HTTP_201_CREATED)
