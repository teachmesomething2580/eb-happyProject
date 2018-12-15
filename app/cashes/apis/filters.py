import django_filters

from cashes.models import Cash


class CashFilter(django_filters.FilterSet):
    class Meta:
        model = Cash
        fields = {
            'created_at': ['lte', 'gte'],
            'hammer_or_cash': ['exact', ],
            'use_or_save': ['exact', ],
        }