from django.conf import settings
from django.db import models, transaction


class DefaultCash(models.Model):
    USE_OR_SAVE_CHOICES = (
        ('u', 'use'),
        ('s', 'save'),
    )

    content = models.CharField(
        max_length=20,
    )
    amount = models.IntegerField()
    use_or_save = models.CharField(
        choices=USE_OR_SAVE_CHOICES,
        max_length=1,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_user_id",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Hammer(DefaultCash):
    @staticmethod
    @transaction.atomic
    def give_hammer_point(user, amount):

        hammer = Hammer(
            content='회원가입 첫 500원',
            amount=amount,
            use_or_save='s',
            user_id=user
        )

        hammer.save()
        user.hammer += amount
        user.save()


class HappyCash(DefaultCash):
    @staticmethod
    @transaction.atomic
    def give_happy_cash_point(user, amount):

        happy_cash = HappyCash(
            content='회원가입 첫 500원',
            amount=amount,
            use_or_save='s',
            user_id=user
        )

        happy_cash.save()
        user.happy_cash += amount
        user.save()
