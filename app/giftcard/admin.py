from django.contrib import admin

# Register your models here.
from giftcard.models import GiftCardType, OrderGiftCard, PINGiftCard

admin.site.register(GiftCardType)
admin.site.register(OrderGiftCard)
admin.site.register(PINGiftCard)