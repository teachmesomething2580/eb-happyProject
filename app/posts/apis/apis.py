from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers
from rest_framework.filters import SearchFilter, OrderingFilter

from posts.apis.filters import FAQFilter, NoticeFilter
from posts.apis.pagination import FAQPagination
from posts.apis.serializer import NoticeSerializer, FAQSerializer, InquirySerializer, FAQCategorySerializer, \
    NoticeCategorySerializer
from posts.models import Notice, FAQ, Inquiry, FAQCategory, FAQSubCategory, NoticeCategory


class NoticeListAPIView(generics.ListAPIView):
    queryset = Notice.objects.select_related('category')
    serializer_class = NoticeSerializer
    pagination_class = FAQPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_class = NoticeFilter


class FAQListAPIView(generics.ListAPIView):
    queryset = FAQ.objects.all().select_related('category')
    serializer_class = FAQSerializer
    pagination_class = FAQPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_class = FAQFilter


class InquiryCreateListAPIView(generics.ListCreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = FAQPagination

    def perform_create(self, serializer):
        try:
            pk = self.request.data.pop('category')
            f = FAQSubCategory.objects.get(pk=pk)
            serializer.save(user=self.request.user, category=f)
        except FAQSubCategory.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Cateogry가 제공되지 않았거나 잘못된 정보가 전달되었습니다.'})
        except KeyError:
            raise serializers.ValidationError({'detail': 'Cateogry가 제공되지 않았거나 잘못된 정보가 전달되었습니다.'})
        # Error 발생지점

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class FAQCategoryListAPIView(generics.ListAPIView):
    queryset = FAQCategory.objects.prefetch_related('sub_category')
    serializer_class = FAQCategorySerializer


class NoticeCategoryListAPIView(generics.ListAPIView):
    queryset = NoticeCategory.objects.all()
    serializer_class = NoticeCategorySerializer