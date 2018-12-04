from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from cashes.apis.backends import IamPortAPI
from cashes.apis.pagination import CashResultSetPagination
from cashes.apis.permissions import IsAuthenticatedWithPurchase
from giftcard.apis.serializer import GiftCardTypeSerializer, EmailOrderGiftCardSerializer, \
    SMSOrderGiftCardSerializer, AddressOrderGiftCardSerializer, OrderGiftCardSerializer
from giftcard.models import GiftCardType, OrderGiftCard


class GiftCardTypeListAPIView(generics.ListAPIView):
    queryset = GiftCardType.objects.all()
    serializer_class = GiftCardTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_hotdeal', )


class OrderGiftCardPurchaseView(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        # 필수로 가져와야하는 항목을 가져온다.
        imp_uid = request.data['imp_uid']
        try:
            merchant_uid = request.data['merchant_uid']
            paid_amount = request.data['paid_amount']
        except KeyError:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})

        # IamPort의 access_token을 생성하고 위변조를 검사한다.
        result = IamPortAPI().inquiry_purchase_info(imp_uid, paid_amount)
        result_status = result['status']

        full_amount = 0

        if result_status == 'success':
            purchase = request.data['purchase']
            delivery_type = purchase['delivery_type']
            purchase_list = purchase['purchase_list']

            # 상품권 개수 변조 확인
            for p in purchase_list:
                for price in p['giftcard_info']:
                    amount = price['amount']
                    g = GiftCardType.objects.get(gift_card_unique_id=price['type'])
                    if g is None:
                        IamPortAPI().purchase_cancel(imp_uid)
                        raise serializers.ValidationError('해당 GiftCard 종류가 존재하지 않습니다.')
                    full_amount += g.amount * int(amount)

            if full_amount != paid_amount:
                IamPortAPI().purchase_cancel(imp_uid)
                raise serializers.ValidationError('값이 변조되었습니다.')

            if delivery_type == 'email':
                serializer_class = EmailOrderGiftCardSerializer
                extra_field = 'email'
            elif delivery_type == 'sms':
                serializer_class = SMSOrderGiftCardSerializer
                extra_field = 'phone'
            elif delivery_type == 'address':
                serializer_class = AddressOrderGiftCardSerializer
                extra_field = ''
                # 추후 변경성
            else:
                raise serializers.ValidationError({'detail': '해당 상품권 배송 방법은 존재하지 않습니다..'})

            # 객체 생성
            order = OrderGiftCard.create_order(serializer_class, extra_field, imp_uid, merchant_uid, purchase_list, request.user)
            serializer = serializer_class(order, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '값이 변조되었습니다.'})


class OrderGiftCardListView(generics.ListAPIView):
    queryset = OrderGiftCard.objects.all()
    serializer_class = OrderGiftCardSerializer
    pagination_class = CashResultSetPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)
