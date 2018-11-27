from rest_framework import generics

from use_point.apis.pagination import UsePointResultSetPagination
from use_point.apis.serializers import UsePointSerializer
from use_point.models import UsePoint


class UsePointListGenericAPIView(generics.ListAPIView):
    queryset = UsePoint.objects.all()
    serializer_class = UsePointSerializer
    pagination_class = UsePointResultSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        point = self.request.query_params.get('point', 'online')
        if point == 'offline':
            queryset = queryset.filter(is_online=False)
        elif point == 'online':
            queryset = queryset.filter(is_online=True)
        return queryset