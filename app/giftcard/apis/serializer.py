from rest_framework import serializers

from giftcard.models import GiftCardType


class GiftCardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardType
        exclude = (
            'is_active'
        )
        depth = 1
