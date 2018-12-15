from django.urls import path

from giftcard.apis import apis


urlpatterns = [
    path('', apis.GiftCardTypeListAPIView.as_view()),
    path('before-purchase/', apis.BeforeOrderGiftCardPurchaseView.as_view()),
    path('after-purchase/', apis.OrderGiftCardPurchaseView.as_view()),
    path('purchase-list/', apis.OrderGiftCardListView.as_view()),
    path('happy-giftcard/', apis.HappyGiftCardListAPIView.as_view()),
    path('pin-list/', apis.OrderGiftCardWithPINListView.as_view()),
]
