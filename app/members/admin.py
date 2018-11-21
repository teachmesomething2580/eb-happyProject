from django.contrib import admin
from django.contrib.auth import get_user_model

from members.models import Rating

User = get_user_model()

# Register your models here.
admin.site.register(User)
admin.site.register(Rating)
