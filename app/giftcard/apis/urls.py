from django.urls import path

from giftcard.apis import apis

urlpatterns = [
    path('', apis.GiftCardTypeListAPIView.as_view())
]
