import json

import requests
from django.conf import settings


class IamPortAPI:
    def __init__(self):
        self.access_token = None

    def get_access_token(self):
        """
        IamPort 에서 AccessToken을 가져오는 함수

        """
        url = 'https://api.iamport.kr/users/getToken'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'imp_key': settings.SECRET_JSON['IAMPORT_REST_API_KEY'],
            'imp_secret': settings.SECRET_JSON['IAMPORT_REST_API_SECRET_KEY']
        }

        res = requests.post(url, headers=headers, data=json.dumps(data))
        self.access_token = json.loads(res.content)['response']['access_token']
        return self.access_token

    def inquiry_purchase_info(self, imp_uid, browser_amount):
        """
        위변조를 검사하는 함수

        :param imp_uid: 결제 코드
        :param browser_amount: 브라우저에서 요청한 값
        :return:
        """
        self.get_access_token()
        url = 'https://api.iamport.kr/payments/'+imp_uid
        headers = {
            'Authorization': self.access_token
        }
        res = requests.get(url, headers=headers)
        paymentData = json.loads(res.content)

        amountToBePaid = paymentData['response']['amount']

        # 값 위변조 검증
        if browser_amount == amountToBePaid:
            return {'status': 'success', 'message': '일반 결제 성공'}
        else:
            return {'status': 'forgery', 'message': '위변조 결제시도'}

    def purchase_cancel(self, imp_uid):
        """
        결제 취소 함수

        :param imp_uid: 결제 코드
        :return:
        """
        self.get_access_token()
        url = "https://api.iamport.kr/payments/cancel"
        headers = {
            'Authorization': self.access_token
        }
        data = {
            'imp_uid': imp_uid,
        }
        res = requests.post(url, headers=headers, data=data)