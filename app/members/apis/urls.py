from django.urls import path

from members.apis import apis

urlpatterns = [
    path('', apis.UserListGenericAPIView.as_view()),
    path('get/', apis.UserRetrieveGenericAPIView.as_view()),
    path('get/<int:pk>/', apis.UserRetrieveGenericAPIView.as_view()),
    path('auth-token/', apis.AuthTokenView.as_view()),
    path('create-user/', apis.UserCreateGenericAPIView.as_view()),
]