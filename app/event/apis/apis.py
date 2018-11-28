from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from event.apis.pagination import EventResultSetPagination
from event.apis.serializer import EventSerializer
from event.models import Event


class EventCreateListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventResultSetPagination

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise ValidationError('관리자가 아닙니다.')
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', 'all')
        if category == 'all':
            return queryset
        return queryset.filter(category=category)