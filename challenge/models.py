from django.db import models
from django.conf import settings


class Problem(models.Model):
    """문제 정보를 저장하는 모델"""

    PLATFORM_CHOICES = [
        ("BAEKJOON", "백준"),
        ("PROGRAMMERS", "프로그래머스"),
        ("LEETCODE", "리트코드"),
    ]

    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChallengeGroup(models.Model):
    """챌린지 그룹 정보를 저장하는 모델"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="GroupMembership", related_name="groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """그룹 멤버십 정보를 저장하는 모델"""

    ROLE_CHOICES = [
        ("ADMIN", "관리자"),
        ("MEMBER", "멤버"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(ChallengeGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="MEMBER")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "group"]


class Challenge(models.Model):
    """챌린지 정보를 저장하는 모델"""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    group = models.ForeignKey(
        ChallengeGroup, on_delete=models.CASCADE, related_name="challenges"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_challenges",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} ({self.group.name})"


class ChallengeDay(models.Model):
    """챌린지 일차별 문제 정보를 저장하는 모델"""

    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name="challenge_days"
    )
    date = models.DateField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_problems",
    )

    class Meta:
        unique_together = ["challenge", "date"]
        ordering = ["date"]

    def __str__(self):
        return f"Day {self.date} - {self.problem.title}"


class Solution(models.Model):
    """사용자의 문제 풀이 현황을 저장하는 모델"""

    STATUS_CHOICES = [
        ("SOLVED", "해결"),
        ("FAILED", "실패"),
        ("SKIPPED", "건너뜀"),
        ("IN_PROGRESS", "진행 중"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge_day = models.ForeignKey(
        ChallengeDay, on_delete=models.CASCADE, related_name="solutions"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    solution_link = models.URLField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "challenge_day"]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.user.username} - Day {self.challenge_day.date}"

