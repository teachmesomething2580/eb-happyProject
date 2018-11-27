from django.urls import path

from cashes.apis import apis

urlpatterns = [
    path('purchase/', apis.CashPurchaseGetRequest.as_view()),
    path('purchase-list/', apis.CashPurchaseListView.as_view()),
    path('purchase-giftcard/', apis.OrderCashToGiftCard.as_view()),
]