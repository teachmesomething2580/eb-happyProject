from django.conf import settings
from django.db import models


class UsePoint(models.Model):
    name = models.CharField(
        max_length=50,
    )
    category = models.ForeignKey(
        'UsePointCategory',
        on_delete=models.CASCADE,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    is_online = models.BooleanField(default=False)
    where_to_use = models.OneToOneField(
        'Usage',
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    site = models.TextField()
    shop_image = models.ImageField(
        upload_to='images/shop_image',
        # for Debug
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('name', 'is_online')

    def __str__(self):
        return self.name


class Usage(models.Model):
    is_fee = models.BooleanField(default=False)
    is_import_point = models.BooleanField(default=False)
    month_pay_limit = models.IntegerField(default=0)


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
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class UsePointCategory(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name
