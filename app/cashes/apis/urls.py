from django.urls import path

from cashes.apis import apis

urlpatterns = [
    path('purchase/', apis.CashPurchaseListCreateView.as_view()),
]