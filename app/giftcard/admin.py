from django.contrib import admin

# Register your models here.
from giftcard.models import GiftCard, GiftCardType

admin.site.register(GiftCard)
admin.site.register(GiftCardType)