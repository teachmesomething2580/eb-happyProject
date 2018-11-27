from django.urls import path

from giftcard.apis import apis

urlpatterns = [
    path('', apis.GiftCardTypeListAPIView.as_view()),
    path('purchase/', apis.OrderGiftCardPurchaseView.as_view()),
    path('purchase-list/', apis.OrderGiftCardListView.as_view()),
]
