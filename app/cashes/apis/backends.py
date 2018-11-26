import json

import requests
from django.conf import settings


class IamPortAPI:
    def __init__(self):
        self.access_token = None

    def get_access_token(self):
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
        self.get_access_token()
        url = "https://api.iamport.kr/payments/cancel"
        headers = {
            'Authorization': self.access_token
        }
        data = {
            'imp_uid': imp_uid,
        }
        res = requests.post(url, headers=headers, data=data)
        first = json.loads(res.content)
        a = 1
        print(a)