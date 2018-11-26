from django.contrib import admin

# Register your models here.
from giftcard.models import GiftCardType, OrderGiftCard

admin.site.register(GiftCardType)
admin.site.register(OrderGiftCard)