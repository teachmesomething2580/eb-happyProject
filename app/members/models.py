from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from members.manager import UserAdminManager, UserNormalManager


class Rating(models.Model):
    RATING_CHOICES = (
        ('1', '루키몽'),
        ('2', '실버몽'),
        ('3', '골드몽'),
        ('4', '파워몽'),
        ('5', '슈퍼몽')
    )

    rating_choices_name = models.CharField(
        choices=RATING_CHOICES,
        max_length=1,
        unique=True,
    )
    ticket_count = models.IntegerField()
    cash_count = models.IntegerField()
    charge_support_benefit = models.IntegerField(blank=True, null=True)
    rating_achieve_benefit = models.IntegerField(blank=True, null=True)
    happy_day_benefit = models.IntegerField(blank=True, null=True)
    hammer_benefit = models.IntegerField(blank=True)
    birthday_benefit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.rating_choices_name


class User(AbstractUser):
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    birth = models.DateField(
        # for Debug
        blank=True,
        null=True,
    )
    sns_agree = models.BooleanField(default=False)
    email_agree = models.BooleanField(default=False)
    online_available_use_category_limit = models.ManyToManyField(
        'use_point.UsePointCategory',
        blank=True,
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


class Address(models.Model):
    postcode = models.CharField(max_length=5)
    address = models.TextField()
    detail = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
