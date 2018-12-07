from django.urls import path

from use_point.apis import apis

urlpatterns = [
    path('', apis.UsePointListGenericAPIView.as_view()),
    path('<int:pk>/', apis.UsePointRetrieveGenericAPIView.as_view()),
    path('import', apis.CategoryUsePointListGenericAPIView.as_view()),
    path('category/', apis.CategoryListGenericAPIView.as_view()),
    path('like/', apis.UsePointLikeGenericAPIView.as_view()),
]