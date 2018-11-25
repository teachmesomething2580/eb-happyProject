from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from use_point.models import UsePoint

User = get_user_model()


class GiftCardType(models.Model):
    available_day_limit = models.DateTimeField()
    amount = models.IntegerField()
    is_hotdeal = models.BooleanField(default=False)
    use_point = models.ForeignKey(
        UsePoint,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        try:
            use_point = self.use_point.name
        except AttributeError:
            use_point = '해피머니'
        return use_point + ' '+str(self.amount)+'원권'


class GiftCard(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    pin = models.CharField(max_length=18)
    is_used = models.BooleanField(default=False)
    gift_card = models.ForeignKey(
        GiftCardType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.pin


class OrderGiftCard(models.Model):
    numbering = models.CharField(max_length=20)
    order_with = models.ManyToManyField(
        'self',
        blank=True,
    )
    gift_card_type = models.ManyToManyField(
        'GiftCardType',
    )
    order_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        choices=(
            ('d', '택배 선물'),
            ('e', '이메일'),
            ('s', 'SMS'),
            ('b', '영수증'),
            ('m1', '모바일 상품권'),
            ('m2', '사용처 전용 모바일 상품권'),
        ),
        max_length=2,
    )
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)