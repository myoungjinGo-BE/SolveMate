from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from challenge.models import (
    Problem,
    ChallengeGroup,
    ChallengeDay,
    Solution,
    Challenge,
)
from .serializers import (
    ProblemSerializer,
    ChallengeGroupSerializer,
    ChallengeSerializer,
    ChallengeDaySerializer,
    SolutionSerializer,
)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Problem.objects.all()
        platform = self.request.query_params.get("platform", None)
        if platform:
            queryset = queryset.filter(platform=platform)
        return queryset


class ChallengeGroupViewSet(viewsets.ModelViewSet):
    queryset = ChallengeGroup.objects.all()
    serializer_class = ChallengeGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ChallengeDayViewSet(viewsets.ModelViewSet):
    queryset = ChallengeDay.objects.all()
    serializer_class = ChallengeDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ChallengeDay.objects.all()
        challenge_id = self.request.query_params.get("challenge", None)
        if challenge_id:
            queryset = queryset.filter(challenge_id=challenge_id)
        return queryset


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Solution.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
