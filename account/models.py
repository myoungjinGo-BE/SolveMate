from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from challenge.models import GroupMembership


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    profile_picture = models.URLField(null=True)
    kakao_id = models.CharField(max_length=100, null=True, blank=True, unique=True)

    USERNAME_FIELD = "nickname"

    @property
    def default_group(self):
        # 사용자가 속한 첫 번째 그룹을 기본 그룹으로 반환
        return GroupMembership.objects.filter(user=self).first().group
