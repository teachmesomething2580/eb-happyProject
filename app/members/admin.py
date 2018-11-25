from django.contrib import admin
from django.contrib.auth import get_user_model

from members.models import Rating, Address

User = get_user_model()

# Register your models here.
admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Address)