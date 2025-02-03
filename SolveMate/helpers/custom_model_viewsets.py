from rest_framework import status
from rest_framework import viewsets

from SolveMate.helpers.response_helpers import ResponseHelper


class CustomModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet의 응답을 커스터마이징하는 Mixin 클래스
    """

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return ResponseHelper.success(
            data=response.data, status_code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return ResponseHelper.success(data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return ResponseHelper.success(data=response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return ResponseHelper.success(data=response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return ResponseHelper.success(
            message="Resource deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ResponseHelper.success(data=response.data)
