from django.contrib.auth.models import UserManager

from cashes.models import Hammer


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)

        # 회원가입시 500 Hammer 증정
        Hammer.give_hammer_point(
            content='회원가입 500원',
            amount=500,
            use_or_save='s',
            user_id=user,
        )
        return user
