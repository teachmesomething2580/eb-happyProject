from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class ABCPosts(models.Model):
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField()
    view = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Notice(ABCPosts):
    category = models.ForeignKey(
        'NoticeCategory',
        on_delete=models.CASCADE,
    )
    is_hot = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FAQ(ABCPosts):
    category = models.ForeignKey(
        'FAQSubCategory',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'FAQSubCategory',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    file = models.FileField(
        upload_to='files',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-pk']


class NoticeCategory(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class FAQCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class FAQSubCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    main_category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
        related_name='sub_category'
    )

    def __str__(self):
        return self.name