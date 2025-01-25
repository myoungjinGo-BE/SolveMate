from rest_framework.response import Response
from rest_framework import status


class ResponseHelper:
    default_success_message = "Operation succeeded"
    default_error_message = "An error occurred"

    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        성공 응답을 반환하는 메서드
        """
        return Response(
            {
                "status": "success",
                "message": message or ResponseHelper.default_success_message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def error(message=None, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        에러 응답을 반환하는 메서드
        """
        return Response(
            {
                "status": "error",
                "message": message or ResponseHelper.default_error_message,
                "errors": errors,
            },
            status=status_code,
        )
