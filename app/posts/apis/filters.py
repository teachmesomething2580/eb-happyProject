import django_filters
from django.db import models
from django.db.models import Q

from event.models import Event
from posts.models import FAQ


class CategoryFilterList(django_filters.Filter):
    def __init__(self, name, lookup_type, *args, **kwargs):
        self.name = name
        self.lookup_type = lookup_type
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.name, self.lookup_type): values})
        return qs


class FAQFilter(django_filters.FilterSet):
    category__names = CategoryFilterList(name="category__name", lookup_type='in')
    contain_contents = django_filters.CharFilter(method='filter_contain_comments')

    class Meta:
        model = FAQ
        fields = {
            'category__name': ['exact', ],
            'category__names': ['exact', ],
        }

    def filter_contain_comments(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )