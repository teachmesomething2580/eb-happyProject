from rest_framework import serializers

from ..models import GiftCardType, OrderGiftCard, EmailOrderGiftCard, SMSOrderGiftCard, AddressOrderGiftCard, \
    HappyGiftCard, PINGiftCard, OrderGiftCardAmount


class HappyGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HappyGiftCard
        fields = '__all__'


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


class OrderGiftCardWithPINSerializer(serializers.ModelSerializer):
    created_in_order = serializers.SerializerMethodField()

    class Meta:
        model = PINGiftCard
        fields = (
            'PIN',
            'is_used',
            'created_in_order',
            'created_at',
        )

    def get_created_in_order(self, obj):
        serializer_context = {'delivery_type': self.context.get('delivery_type')}
        order_gift_amount = OrderGiftCardAmount.objects.get(pingiftcard=obj)
        serializer = OrderGiftCardAmountSerializer(order_gift_amount, context=serializer_context)
        return serializer.data


class OrderGiftCardAmountSerializer(serializers.ModelSerializer):
    gift_card = HappyGiftCardSerializer()
    order_gift_card = serializers.SerializerMethodField()

    class Meta:
        model = OrderGiftCardAmount
        fields = (
            'gift_card',
            'order_gift_card',
            'amount',
        )

    def get_order_gift_card(self, obj):
        delivery_type = self.context.get('delivery_type')

        if delivery_type == 'email':
            serializer_class = EmailOrderGiftCardSerializer
            queryset = EmailOrderGiftCard
            extra_field = 'email'
        elif delivery_type == 'sms':
            serializer_class = SMSOrderGiftCardSerializer
            queryset = SMSOrderGiftCard
            extra_field = 'sms'
        elif delivery_type == 'address':
            serializer_class = AddressOrderGiftCardSerializer
            queryset = AddressOrderGiftCard
            extra_field = ''
        else:
            raise serializers.ValidationError({'detail': '해당 배송방법이 존재하지 않습니다.'})

        order_gift_card = queryset.objects.get(ordergiftcardamount=obj)
        serializer = serializer_class(order_gift_card)
        return serializer.data


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
