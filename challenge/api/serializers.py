from rest_framework import serializers

from challenge.models import (
    Problem,
    GroupMembership,
    ChallengeGroup,
    ChallengeDay,
    Solution,
    ChallengeParticipant,
    Challenge,
)


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "title", "platform", "link", "created_at"]


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ["id", "user", "group", "role", "joined_at", "is_active"]


class ChallengeGroupSerializer(serializers.ModelSerializer):
    members = GroupMembershipSerializer(
        source="groupmembership_set", many=True, read_only=True
    )

    class Meta:
        model = ChallengeGroup
        fields = ["id", "name", "description", "created_at", "created_by", "members"]


class ChallengeDaySerializer(serializers.ModelSerializer):
    problem_detail = ProblemSerializer(source="problem", read_only=True)

    class Meta:
        model = ChallengeDay
        fields = ["id", "day_number", "date", "problem", "problem_detail", "author"]


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            "id",
            "user",
            "challenge_day",
            "status",
            "solution_link",
            "submitted_at",
            "updated_at",
        ]


class ChallengeParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeParticipant
        fields = ["id", "user", "challenge", "joined_at", "is_active"]


class ChallengeSerializer(serializers.ModelSerializer):
    challenge_days = ChallengeDaySerializer(many=True, read_only=True)
    participants = ChallengeParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = [
            "id",
            "title",
            "description",
            "group",
            "start_date",
            "end_date",
            "created_by",
            "created_at",
            "is_active",
            "challenge_days",
            "participants",
        ]
