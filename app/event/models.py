from django.db import models


class Event(models.Model):
    CATEGORY_CHOICES = (
        ('happy', '해피머니 이벤트'),
        ('join', '참여 이벤트'),
        ('invite', '초대 이벤트'),
        ('cashback', '캐시백 이벤트'),
        ('alliance', '제휴 이벤트'),
        ('entry', '응모 이벤트'),
        ('comment', '댓글 이벤트'),
    )

    title = models.CharField(max_length=100, unique=True)
    start = models.DateField()
    end = models.DateField()
    category = models.CharField(
        max_length=12,
        choices=CATEGORY_CHOICES,
    )
    tag = models.CharField(
        max_length=12,
    )
    general_image = models.ImageField(
        upload_to='images/event',
    )
    banner = models.ImageField(
        upload_to='images/event',
        blank=True,
        null=True,
    )

    site_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    content_image = models.ImageField(
        upload_to='images/event',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title