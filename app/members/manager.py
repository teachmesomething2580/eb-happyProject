from django.contrib.auth.models import UserManager

from cashes.models import Hammer


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)
        Hammer.give_hammer_point(user, 500)
        return user