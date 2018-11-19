from django.urls import path

from members.apis import apis

urlpatterns = [
    path('', apis.UserListGenericAPIView.as_view())
]