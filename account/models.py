from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    profile_picture = models.URLField(null=True)
    kakao_id = models.CharField(max_length=100, null=True, blank=True, unique=True)

    USERNAME_FIELD = "nickname"
