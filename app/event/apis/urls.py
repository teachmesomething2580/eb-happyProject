from django.urls import path

from event.apis import apis

urlpatterns = [
    path('', apis.EventCreateListAPIView.as_view()),
]