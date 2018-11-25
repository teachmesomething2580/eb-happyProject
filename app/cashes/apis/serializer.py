from rest_framework import serializers

from cashes.models import Cash


class CashPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        exclude = (
            'user',
        )
