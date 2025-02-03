from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from SolveMate.helpers.response_helpers import ResponseHelper
from challenge.models import Problem
from challenge.serializers import ProblemSerializer, ProblemSearchSerializer


class ProblemViewSet(viewsets.GenericViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @method_decorator(cache_page(60 * 5))
    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        문제 검색 API
        Query Parameter:
        - query: 검색할 문제 제목
        """
        search_serializer = ProblemSearchSerializer(data=request.query_params)
        if not search_serializer.is_valid():
            return Response(
                search_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        query = search_serializer.validated_data["query"]

        # 검색어가 없는 경우 빈 결과 반환
        if not query:
            return ResponseHelper.success([])

        problems_by_title = self.get_queryset().filter(title__icontains=query)
        problems_by_problem_id = self.get_queryset().filter(problem_id__icontains=query)
        problems = problems_by_title.union(problems_by_problem_id)

        page = self.paginate_queryset(problems)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(problems, many=True)
        return ResponseHelper.success(serializer.data)
