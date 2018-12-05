from rest_framework.filters import OrderingFilter
from django_filters import FilterSet


class UsePointOrdering(OrderingFilter):
    def remove_invalid_fields(self, queryset, fields, view, request):
        ordering = super().remove_invalid_fields(queryset, fields, view, request)
        for field in fields:
            if 'like_users_count' in field:
                ordering.append(field)
        return ordering

