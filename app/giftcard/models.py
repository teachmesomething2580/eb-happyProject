from django.conf import settings
from django.db import models

from use_point.models import UsePoint


class GiftCardType(models.Model):
    available_day_limit = models.IntegerField()
    amount = models.IntegerField()
    is_hotdeal = models.BooleanField(default=False)
    use_point = models.ForeignKey(
        UsePoint,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.use_point.name+' '+str(self.amount)+'원권'


class GiftCard(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    pin = models.CharField(max_length=18)
    is_used = models.BooleanField(default=False)
    gift_card = models.ForeignKey(
        GiftCardType,
        on_delete=models.CASCADE,
    )