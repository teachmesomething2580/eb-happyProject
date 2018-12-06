import django_filters
from django.db import models

from use_point.models import UsePoint


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


class ProductFilter(django_filters.FilterSet):
    category__names = CategoryFilterList(name="category__name", lookup_type='in')

    class Meta:
        model = UsePoint
        fields = {
            'name': ['exact', 'contains', ],
            'category__name': ['exact', ],
            'category__names': ['exact', ],
            'is_online': ['exact', ],
        }