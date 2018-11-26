from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from use_point.models import UsePoint

User = get_user_model()


class GiftCardCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    shop_image = models.ImageField(
        upload_to='images/shop_image',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class GiftCardType(models.Model):
    CATEGORY_CHOICE = (
        ('h', 'hot'),
        ('m', 'mobile'),
    )

    amount = models.IntegerField()
    is_hotdeal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICE,
    )
    mall_category = models.ForeignKey(
        GiftCardCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.mall_category.name) + ' ' + str(self.amount)+'원권'


class OrderGiftCardAmount(models.Model):
    gift_card = models.ForeignKey(
        GiftCardType,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()


class OrderGiftCard(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    gift_card = models.ForeignKey(
        OrderGiftCardAmount,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=100,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15)


class EmailOrderGiftCard(OrderGiftCard):
    email = models.EmailField()


class SMSOrderGiftCard(OrderGiftCard):
    phone = PhoneNumberField()