from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers

from event.apis.filters import EventFilter
from event.apis.pagination import EventResultSetPagination
from event.apis.serializer import EventSerializer
from event.models import Event


class EventCreateListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventResultSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = EventFilter

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise serializers.ValidationError({'detail': '관리자가 아닙니다.'})
        serializer.save()