from django.conf import settings
from django.db import models, transaction
from rest_framework import serializers

from cashes.manager import CashManager


class Cash(models.Model):

    objects = CashManager()

    USE_OR_SAVE_CHOICES = (
        ('u', 'use'),
        ('s', 'save'),
    )
    HAMMER_OR_HAPPY = (
        ('hc', 'HappyCash'),
        ('hm', 'Hammer'),
    )

    merchant_uid = models.CharField(
        max_length=100,
    )
    amount = models.PositiveIntegerField()
    hammer_or_cash = models.CharField(
        choices=HAMMER_OR_HAPPY,
        max_length=3,
    )
    use_or_save = models.CharField(
        choices=USE_OR_SAVE_CHOICES,
        max_length=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_user",
        on_delete=models.CASCADE,
    )
    purchased = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.user.username + "님에게 " + self.get_hammer_or_cash_display() + "를 " + str(self.amount) + "만큼 " + ('저장' if self.use_or_save == 's' else '사용')

    @staticmethod
    @transaction.atomic
    def change_point(**kwargs):
        user = kwargs.pop('user')
        amount = int(kwargs.pop('amount'))

        if user.hammer - amount < 0:
            raise serializers.ValidationError({'detail': '잔액이 부족합니다.'})

        hammer = Cash(
            merchant_uid='해머 전환',
            amount=amount,
            hammer_or_cash='hm',
            use_or_save='u',
            user=user,
        )

        cash = Cash(
            merchant_uid='해머 전환',
            amount=amount,
            hammer_or_cash='hc',
            use_or_save='s',
            user=user,
        )

        user.hammer -= amount
        user.happy_cash += amount

        hammer.save()
        cash.save()
        user.save()

        return cash

    @staticmethod
    @transaction.atomic
    def give_point(**kwargs):

        cash = Cash(
            **kwargs,
        )

        user = kwargs.pop('user')
        amount = int(kwargs.pop('amount'))
        hammer_or_cash = cash.hammer_or_cash

        if cash.use_or_save == 'u':
            if user.happy_cash - amount < 0:
                raise serializers.ValidationError({'detail': '잔액이 부족합니다.'})

            if hammer_or_cash == 'hm':
                if user.hammer - amount < 0:
                    raise serializers.ValidationError({'detail': '잔액이 부족합니다.'})
                user.hammer -= amount
            else:
                user.happy_cash -= amount
        else:
            if hammer_or_cash == 'hm':
                user.hammer += amount
            else:
                user.happy_cash += amount

        cash.save()
        user.save()

        return cash
