from rest_framework import serializers

from account.models import User


class SignUpSerializer(serializers.ModelSerializer):
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
