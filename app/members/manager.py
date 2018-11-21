from django.contrib.auth.models import UserManager

from cashes.models import Hammer


class UserIntegrationManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        from members.models import Rating

        extra_fields['rating'] = Rating.objects.filter(name='루키몽')[0]
        user = super().create_user(username, email, password, **extra_fields)

        # 회원가입시 500 Hammer 증정
        Hammer.give_hammer_point(
            content='회원가입 500원',
            amount=500,
            use_or_save='s',
            user_id=user,
        )
        return user


class UserAdminManager(UserIntegrationManager):
    """
    Admin Manager
    """
    def get_queryset(self):
        return super().get_queryset().all()


class UserNormalManager(UserIntegrationManager):
    """
    User Manager
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)