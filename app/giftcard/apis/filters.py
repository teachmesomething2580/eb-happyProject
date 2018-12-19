import django_filters

from giftcard.models import OrderGiftCard


class OrderGiftCardFilter(django_filters.FilterSet):
    class Meta:
        model = OrderGiftCard
        fields = {
            'merchant_uid': ['contains', ],
            'created_at': ['lte', 'gte'],
            'is_purchase': ['exact', ],
            'delivery_type': ['exact', ],
        }