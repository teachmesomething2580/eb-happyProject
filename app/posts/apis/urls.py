from django.urls import path

from posts.apis import apis

urlpatterns = [
    path('notice/', apis.NoticeListAPIView.as_view()),
    path('faq/', apis.FAQListAPIView.as_view()),
    path('inquiry/', apis.InquiryCreateListAPIView.as_view()),
    path('faq-category/', apis.FAQCategoryListAPIView.as_view()),
    path('notice-category/', apis.NoticeCategoryListAPIView.as_view()),
]