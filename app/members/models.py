from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from members.manager import UserAdminManager, UserNormalManager


class User(AbstractUser):
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    sns_agree = models.BooleanField(default=False)
    email_agree = models.BooleanField(default=False)
    online_available_use_category_limit = models.ManyToManyField(
        'use_point.Category',
    )
    rating = models.ForeignKey(
        'members.Rating',
        on_delete=models.CASCADE,
        # for Debug
        blank=True,
        null=True,
    )
    hammer = models.PositiveIntegerField(default=0)
    happy_cash = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    adminManager = UserAdminManager()
    normalManager = UserNormalManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Rating(models.Model):
    name = models.CharField(max_length=10)
    ticket_count = models.IntegerField(blank=True)
    cash_count = models.IntegerField(blank=True)
    charge_support_benefit = models.IntegerField(blank=True)
    rating_achieve_benefit = models.IntegerField(blank=True)
    happy_day_benefit = models.IntegerField(blank=True)
    hammer_benefit = models.IntegerField(blank=True)
    birthday_benefit = models.IntegerField(blank=True)
