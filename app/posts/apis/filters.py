import django_filters

from event.models import Event
from posts.models import FAQ


class FAQFilter(django_filters.FilterSet):
    class Meta:
        model = FAQ
        fields = {
            'title': ['exact', 'contains', ],
            'category__name': ['exact', ],
        }