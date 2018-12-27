from django.db import models
from django.db.models import F, Count


class UsePointManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            like_users_count=Count('like_users'),
        )