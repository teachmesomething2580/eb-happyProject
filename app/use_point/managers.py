from django.db import models
from django.db.models import F, Count


class UsePointManager(models.Manager):
    def get_queryset(self):
        return super(UsePointManager, self).get_queryset().annotate(
            like_users_count=Count('like_users'),
        )
