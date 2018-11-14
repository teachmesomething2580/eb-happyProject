from django.contrib import admin

# Register your models here.
from cashes.models import Hammer, HappyCash

admin.site.register(Hammer)
admin.site.register(HappyCash)