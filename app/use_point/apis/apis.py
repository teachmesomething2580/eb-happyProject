from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from use_point.apis.OrderingFilter import UsePointOrdering
from use_point.apis.pagination import UsePointResultSetPagination
from use_point.apis.serializers import UsePointSerializer, CategoryUsePointSerializer, \
    CategorySerializer
from use_point.models import UsePoint, UsePointCategory


class UsePointListGenericAPIView(generics.ListAPIView):
    __basic_fields = ('name', 'is_online', )
    queryset = UsePoint.objects.all()
    serializer_class = UsePointSerializer
    pagination_class = UsePointResultSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, UsePointOrdering)
    filter_fields = __basic_fields
    search_fields = __basic_fields

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context.update({
                'request': self.request
            })
        return context


class CategoryUsePointListGenericAPIView(generics.ListAPIView):
    queryset = UsePointCategory.objects.all()
    serializer_class = CategoryUsePointSerializer


class CategoryListGenericAPIView(generics.ListAPIView):
    queryset = UsePointCategory.objects.all()
    serializer_class = CategorySerializer
