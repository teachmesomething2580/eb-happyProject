import django_filters

from event.models import Event


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'title': ['exact', 'contains', ],
            'category': ['exact', ],
            'end': ['lt', 'gte'],
        }