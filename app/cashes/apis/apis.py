import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from cashes.apis.backends import IamPortAPI
from cashes.apis.filters import CashFilter
from cashes.apis.pagination import CashListPagination
from cashes.apis.permissions import IsAuthenticatedWithPurchase
from cashes.apis.serializer import CashPurchaseSerializer
from cashes.models import Cash
from giftcard.apis.serializer import EmailOrderGiftCardSerializer, SMSOrderGiftCardSerializer, \
    AddressOrderGiftCardSerializer
from giftcard.models import OrderGiftCard, GiftCardType


class CashPurchaseListView(generics.ListAPIView):
    queryset = Cash.objects.all()
    serializer_class = CashPurchaseSerializer
    pagination_class = CashListPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = CashFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


class CashPurchaseGetRequest(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        # 필수로 가져와야하는 항목을 가져온다.
        imp_uid = request.data['imp_uid']
        try:
            paid_amount = request.data['paid_amount']
        except KeyError:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})

        # IamPort의 access_token을 생성하고 위변조를 검사한다.
        result = IamPortAPI().inquiry_purchase_info(imp_uid, paid_amount)
        result_status = result['status']

        if result_status == 'success':
            timestamp = int(datetime.datetime.now().timestamp() * 1000)
            merchant_uid = 'happyCash_' + str(timestamp)
            paid_amount = paid_amount + paid_amount * 0.03

            data = {
                'merchant_uid': merchant_uid,
                'amount': paid_amount,
                'hammer_or_cash': 'hc',
                'use_or_save': 's',
            }
            serializer = CashPurchaseSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Serializer 실패
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '결제 정보 생성시 오류가 발생했습니다..'})
        else:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '값이 변조되었습니다.'})


class OrderHammerToCash(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        try:
            paid_amount = int(request.data['paid_amount'])
        except KeyError:
            raise serializers.ValidationError({'detail': '브라우저의 결제 정보가 포함되지 않았습니다..'})

        if paid_amount < 3000:
            raise serializers.ValidationError({'detail': '3000 해머 이하의 값은 바꿀 수 없습니다..'})

        cash = Cash().change_point(
            amount=paid_amount,
            user=self.request.user,
        )

        serializer = CashPurchaseSerializer(cash)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderCashToGiftCard(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        try:
            purchase = request.data['purchase']
            merchant_uid = request.data['merchant_uid']
            paid_amount = request.data['paid_amount']
        except KeyError:
            return Response(data={'error': 'request Key Error'}, status=status.HTTP_400_BAD_REQUEST)

        delivery_type = purchase['delivery_type']
        purchase_list = purchase['purchase_list']

        full_amount = 0

        # 상품권 개수 변조 확인
        for p in purchase_list:
            for price in p['giftcard_info']:
                amount = price['amount']
                g = GiftCardType.objects.get(gift_card_unique_id=price['type'])
                if g is None:
                    raise serializers.ValidationError('해당 GiftCard 종류가 존재하지 않습니다.')
                full_amount += g.amount * int(amount)

        if full_amount != paid_amount:
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
            return

        # 객체 생성
        order = OrderGiftCard.create_order(serializer_class, extra_field, None, merchant_uid, purchase_list,
                                           request.user, paid_amount)
        serializer = serializer_class(order, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
