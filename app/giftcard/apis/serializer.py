from rest_framework import serializers

from ..models import GiftCardType, OrderGiftCard, EmailOrderGiftCard, SMSOrderGiftCard, AddressOrderGiftCard


class GiftCardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardType
        exclude = (
            'is_active',
        )
        depth = 1


class OrderGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGiftCard
        exclude = (
            'id',
            'user',
        )
        read_only_fields = (
            'created_at',
        )


class EmailOrderGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOrderGiftCard
        exclude = (
            'id',
            'user',
        )
        read_only_fields = (
            'created_at',
        )


class SMSOrderGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSOrderGiftCard
        exclude = (
            'id',
            'user',
        )
        read_only_fields = (
            'created_at',
        )


class AddressOrderGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressOrderGiftCard
        exclude = (
            'id',
            'user',
        )
        read_only_fields = (
            'created_at',
        )
