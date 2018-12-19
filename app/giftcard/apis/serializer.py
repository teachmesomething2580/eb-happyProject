from rest_framework import serializers

from ..models import GiftCardType, OrderGiftCard, HappyGiftCard, PINGiftCard, OrderGiftCardAmount, EmailOrderGiftCard


class PINGiftCardSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = PINGiftCard
        fields = (
            'PIN',
            'is_used',
            'created_at',
            'price'
        )

    def get_price(self, obj):
        order_gift_amount = OrderGiftCardAmount.objects.get(pingiftcard=obj)
        return order_gift_amount.gift_card.price


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
        serializer_class = OrderGiftCardSerializer
        model_class = OrderGiftCard

        if delivery_type == 'email':
            extra_field = 'email'
        elif delivery_type == 'sms':
            extra_field = 'sms'
        elif delivery_type == 'address':
            extra_field = ''
        else:
            raise serializers.ValidationError({'detail': '해당 배송방법이 존재하지 않습니다.'})

        order_gift_card = model_class.objects.get(ordergiftcardamount=obj)
        serializer = serializer_class(order_gift_card)
        return serializer.data
