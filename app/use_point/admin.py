from django.contrib import admin

# Register your models here.
from use_point.models import UsePoint, GiftCard, GiftCardType, UsePointCategory, Usage

admin.site.register(UsePoint)
admin.site.register(Usage)
admin.site.register(GiftCard)
admin.site.register(GiftCardType)
admin.site.register(UsePointCategory)
