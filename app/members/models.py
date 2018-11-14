from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    name = models.CharField(
        max_length=10,
    )
    phone = PhoneNumberField()
    email = models.EmailField()
    sns_agree = models.BooleanField(blank=True, default=False)
    email_agree = models.BooleanField(blank=True, default=False)
    online_available_use_category_limit = models.CharField(
        choices='',
        max_length=4,
    )
    rating = models.CharField(
        choices='',
        max_length=4,
    )
    hammer = models.PositiveIntegerField(default=0)
    happy_cash = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
