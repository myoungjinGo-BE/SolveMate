from rest_framework import serializers

from account.models import User
from challenge.models import ChallengeGroup


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    kakao_id = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "profile_picture",
            "kakao_id",
        ]


class ChallengeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeGroup
        fields = "__all__"
