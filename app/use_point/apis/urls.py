from django.urls import path

from use_point.apis import apis

urlpatterns = [
    path('', apis.UsePointListGenericAPIView.as_view()),
]