from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Exists, Subquery
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

User = get_user_model()


class UsePointListGenericAPIView(generics.ListAPIView):
    """
    UsePoint List를 전부 내려주는 API
    """
    serializer_class = UsePointSerializer
    pagination_class = UsePointResultSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, UsePointOrdering,)
    filter_class = ProductFilter

    def get_queryset(self):
        queryset = UsePoint.objects \
            .select_related('where_to_use', 'category') \
            .prefetch_related('like_users')
        if self.request.user.is_authenticated:
            user_exists = User.objects.filter(
                pk=self.request.user.pk,
                pk__in=OuterRef('like_users'),
            )
            queryset = queryset.annotate(is_like=Exists(user_exists))
        return queryset


class UsePointRetrieveGenericAPIView(generics.RetrieveAPIView):
    """
    특정 UsePoint API를 내려주는 API
    """
    queryset = UsePoint.objects.all()
    serializer_class = UsePointSerializer

    def get_queryset(self):
        queryset = UsePoint.objects \
            .select_related('where_to_use') \
            .prefetch_related('like_users')
        if self.request.user.is_authenticated:
            # user_exists = User.objects.filter(
            #     pk=self.request.user.pk,
            #     pk__in=OuterRef('like_users'),
            # )
            # queryset = queryset.annotate(is_like=Exists(user_exists))
            queryset = queryset.annotate(is_like=Exists(queryset.filter(like_users__in=self.request.user)))
        return queryset


    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context.update({
                'request': self.request
            })
        return context


class CategoryUsePointListGenericAPIView(generics.ListAPIView):
    """
    Category별로 UsePoint를 내려주는 API
    """

    serializer_class = CategoryUsePointSerializer

    def get_queryset(self):
        queryset = UsePointCategory.objects.prefetch_related(
            'usepoint_set',
            'usepoint_set__like_users',
            'usepoint_set__where_to_use'
        ).filter(
            usepoint__is_online=True,
            usepoint__where_to_use__is_import_point=True,
        ).distinct()

        return queryset


class CategoryListGenericAPIView(generics.ListAPIView):
    """
    Category List를 내려주는 API
    """
    __basic_fields = ('name', 'usepoint__is_online', )
    queryset = UsePointCategory.objects.all().distinct()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filter_fields = __basic_fields
    search_fields = __basic_fields


class UsePointLikeGenericAPIView(APIView):
    """
    UsePoint 좋아요를 설정하는 API
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        serializer = UsePointLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)