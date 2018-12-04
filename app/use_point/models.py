from django.conf import settings
from django.db import models

from use_point.managers import UsePointManager


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

    objects = UsePointManager()

    class Meta:
        unique_together = ('name', 'is_online')
        ordering = ['pk']

    def __str__(self):
        return self.name


class Usage(models.Model):
    is_fee = models.BooleanField(default=False)
    is_import_point = models.BooleanField(default=False)
    month_pay_limit = models.IntegerField(default=0)


class UsePointCategory(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name
