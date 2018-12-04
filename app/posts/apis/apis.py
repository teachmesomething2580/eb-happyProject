from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError

from posts.apis.pagination import PostsResultSetPagination
from posts.apis.serializer import NoticeSerializer, FAQSerializer, InquirySerializer, FAQCategorySerializer
from posts.models import Notice, FAQ, Inquiry, FAQCategory, FAQSubCategory


class NoticeListAPIView(generics.ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = PostsResultSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', 'all')
        if category == 'all':
            return queryset
        return queryset.filter(category__pk=category)


class FAQListAPIView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = PostsResultSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', 'all')
        if category == 'all':
            return queryset
        return queryset.filter(category__pk=category)


class InquiryCreateListAPIView(generics.ListCreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = PostsResultSetPagination

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
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer