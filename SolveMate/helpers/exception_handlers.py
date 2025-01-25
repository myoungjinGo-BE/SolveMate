from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    DRF의 기본 Exception Handler를 커스터마이징하여
    ValidationError 및 기타 예외를 우리가 정의한 형식으로 처리합니다.
    """
    # 먼저 기본 핸들러를 호출하여 기본 응답을 가져옵니다.
    response = exception_handler(exc, context)

    # ValidationError 커스터마이징
    if isinstance(exc, ValidationError):
        custom_response = {
            "status": "error",
            "message": "Validation failed",
            "errors": response.data,  # DRF의 기본 ValidationError 데이터
        }
        return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

    # 기본 핸들러가 처리하지 못한 예외를 우리가 정의한 형식으로 처리
    if response is None:
        return Response(
            {
                "status": "error",
                "message": "Something went wrong",
                "errors": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # 기본 핸들러가 처리한 응답은 그대로 반환
    return response
