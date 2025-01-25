from account.models import User
from challenge.models import ChallengeGroup


class GroupService:
    @staticmethod
    def join_default_group(user: User) -> None:
        """
        기본 그룹을 반환하는 메서드
        """
        default_group = ChallengeGroup.objects.get_or_create(name="기본_그룹")[0]
        default_group.members.add(user)
