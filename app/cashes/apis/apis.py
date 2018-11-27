import json

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cashes.apis.backends import IamPortAPI
from cashes.apis.permissions import IsAuthenticatedWithPurchase
from cashes.apis.serializer import CashPurchaseSerializer
from cashes.models import Cash


class CashPurchaseListView(generics.ListAPIView):
    queryset = Cash.objects.all()
    serializer_class = CashPurchaseSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        h = self.request.query_params.get('h', 'hc')
        return queryset.filter(user=user, hammer_or_cash=h)


class CashPurchaseGetRequest(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        # 필수로 가져와야하는 항목을 가져온다.
        imp_uid = request.data['response']['imp_uid']
        try:
            merchant_uid = request.data['response']['merchant_uid']
            browser_amount = request.data['response']['paid_amount']
        except KeyError:
            IamPortAPI().purchase_cancel(imp_uid)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # IamPort의 access_token을 생성하고 위변조를 검사한다.
        result = IamPortAPI().inquiry_purchase_info(imp_uid, browser_amount)
        result_status = result['status']

        if result_status == 'success':
            data = {
                'content': merchant_uid,
                'amount': browser_amount,
                'hammer_or_cash': 'hc',
                'use_or_save': 's',
            }
            serializer = CashPurchaseSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # serailizer 오류시
            IamPortAPI().purchase_cancel(imp_uid)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # 위변조시
            error_res = {
                'error': result
            }
            IamPortAPI().purchase_cancel(imp_uid)
            return Response(error_res, status=status.HTTP_400_BAD_REQUEST)
