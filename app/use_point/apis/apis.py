from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from use_point.apis.OrderingFilter import UsePointOrdering
from use_point.apis.filters import ProductFilter
from use_point.apis.pagination import UsePointResultSetPagination
from use_point.apis.serializers import UsePointSerializer, CategoryUsePointSerializer, \
    CategorySerializer, UsePointLikeSerializer
from use_point.models import UsePoint, UsePointCategory


class UsePointListGenericAPIView(generics.ListAPIView):
    __basic_fields = ('name', 'is_online', 'category__name', )
    queryset = UsePoint.objects.all()
    serializer_class = UsePointSerializer
    pagination_class = UsePointResultSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, UsePointOrdering,)
    filter_fields = __basic_fields
    search_fields = ('^name', 'is_online', 'category__name', )
    filter_class = ProductFilter

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
    __basic_fields = ('name', 'usepoint__is_online', )
    queryset = UsePointCategory.objects.all().distinct()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filter_fields = __basic_fields
    search_fields = __basic_fields


class UsePointLikeGenericAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        serializer = UsePointLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)