from rest_framework import generics

from use_point.apis.serializers import UsePointSerializer
from use_point.models import UsePoint


class UsePointListGenericAPIView(generics.ListAPIView):
    queryset = UsePoint.objects.all()
    serializer_class = UsePointSerializer
