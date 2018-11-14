from django.contrib import admin

# Register your models here.
from use_point.models import UsePoint, GiftCard, GiftCardType, Category

admin.site.register(UsePoint)
admin.site.register(GiftCard)
admin.site.register(GiftCardType)
admin.site.register(Category)
