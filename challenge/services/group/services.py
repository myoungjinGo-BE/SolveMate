from account.models import User
from challenge.models import ChallengeGroup, GroupMembership


class GroupService:
    DEFAULT_GROUP_NAME = "기본_그룹"

    def join_default_group(self, user: User) -> None:
        """
        기본 그룹을 반환하는 메서드
        """
        default_group = ChallengeGroup.objects.get_or_create(
            name=self.DEFAULT_GROUP_NAME
        )[0]
        default_group.members.add(user)  # 멤버십 DB 등록
