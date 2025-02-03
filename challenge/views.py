from datetime import datetime, timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from SolveMate.helpers.response_helpers import ResponseHelper
from SolveMate.helpers.custom_model_viewsets import (
    CustomModelViewSet,
)
from challenge.models import Problem, ChallengeDay
from challenge.serializers import (
    ProblemSerializer,
    ProblemSearchSerializer,
    ChallengeDaySerializer,
)


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


class ChallengeDayViewSet(CustomModelViewSet):
    queryset = ChallengeDay.objects.all()
    serializer_class = ChallengeDaySerializer

    def get_queryset(self):
        # 현재 로그인한 유저가 속한 그룹의 ChallengeDay만 반환
        user = self.request.user

        # 쿼리 파라미터에서 날짜를 가져옴
        date_str = self.request.query_params.get("date", None)
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                # 날짜 형식이 잘못된 경우 오늘 날짜를 기준으로 설정
                target_date = datetime.now().date()
        else:
            # 쿼리 파라미터가 없는 경우 오늘 날짜를 기준으로 설정
            target_date = datetime.now().date()

        # 기준 날짜를 중심으로 앞뒤 3일씩 총 7일 데이터 필터링
        start_date = target_date - timedelta(days=3)
        end_date = target_date + timedelta(days=3)

        # 기본 그룹의 ChallengeDay만 반환
        return ChallengeDay.objects.filter(
            group=user.default_group, date__range=[start_date, end_date]
        )

    def perform_create(self, serializer):
        # 현재 로그인한 사용자 가져오기
        user = self.request.user

        # serializer에 author와 group 정보 전달
        serializer.save(author=user, group=user.default_group)
