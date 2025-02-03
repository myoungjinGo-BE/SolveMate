from rest_framework import serializers
from challenge.models import ChallengeGroup, Problem


class ChallengeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeGroup
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    """Problem 모델을 위한 시리얼라이저"""

    platform_display = serializers.CharField(
        source="get_platform_display", read_only=True
    )

    class Meta:
        model = Problem
        fields = ["id", "title", "platform", "platform_display", "link", "created_at"]
        read_only_fields = ["created_at"]

    def validate_platform(self, value):
        """플랫폼 선택값 검증"""
        valid_platforms = dict(Problem.PLATFORM_CHOICES).keys()
        if value not in valid_platforms:
            raise serializers.ValidationError(
                f"플랫폼은 {', '.join(valid_platforms)} 중 하나여야 합니다."
            )
        return value


class ProblemSearchSerializer(serializers.Serializer):
    """문제 검색을 위한 시리얼라이저"""

    query = serializers.CharField(required=False, allow_blank=True)
