from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from challenge.models import (
    Problem,
    GroupMembership,
    ChallengeGroup,
    ChallengeDay,
    Solution,
    ChallengeParticipant,
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        group = self.get_object()
        user = request.user

        if not group.groupmembership_set.filter(user=user).exists():
            GroupMembership.objects.create(user=user, group=group)
            return Response({"status": "joined group"})
        return Response(
            {"status": "already a member"}, status=status.HTTP_400_BAD_REQUEST
        )


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        challenge = self.get_object()
        user = request.user

        if not challenge.participants.filter(user=user).exists():
            ChallengeParticipant.objects.create(user=user, challenge=challenge)
            return Response({"status": "joined challenge"})
        return Response(
            {"status": "already participating"}, status=status.HTTP_400_BAD_REQUEST
        )


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
