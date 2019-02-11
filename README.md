# 해피머니 클론 사이트

## 개발환경 소개

```
서비스 개발: python, django
서비스 호스팅: AWS
데이터베이스: Postgresql
배포: AWS ElasticBeanstalk
정적 컨텐츠 처리: AWS S3
버그 레포팅: Sentry
```

## 개발 기간
```
2018-11-9 ~ 2018-12-21
```

## API 리스트

`https://teachmesomething2580.gitbook.io/happymoney/`


## 환경 세팅

```bash
# 개발 모드
export DJANGO_SETTINGS_MODULE=config.settings.dev

# DB 생성 또는 수정사항 적용
# 반드시 Postgresql을 사용하여야한다.
cd app
./manage.py migrate

# 기본 데이터를 위한 데이터 로드 및 크롤링
sh Crawling.sh

# 관리자 생성 (명령어 이후 작성하라는 것 모두 작성)
./manage.py createsuperuser

# 서버 실행
./manage.py runserver
```

## 수정해야할 사항

`+` 는 추가해야할 사항
`*` 은 수정해야할 사항
`-` 는 없애야할 사항

```
+ Query 캐싱
+ 주소 저장, 주소지 상품권 결제
+ Celery, Redis, ElasticbeansTalk Cache를 사용해보기
+ 핀번호 EMAIL 발송

* URL RESTFUL 하게 
* 주문 Model 변경 (현재는 하나의 주문에 여러 사람이 있으면 여러 주문을 생성함)
* FAQ CORS
```

## 결제 값 검증 방법

```
{
	paid_amount: '총 결제량',
	purchase: {
		delivery_type: "sms, email 둘중 하나의 방법",
		purchase_list: [
			name: "받는 사람 이름",
			infoTo: "받는 사람이메일 혹은 전화번호"
			giftcard_info = [
				{
					type: "얼마짜리 상품권",
					amount: "개수"
				},
				...
			],
			...
		]
	}
}
```

1. 결제 전 미리 서버에 결제되어야할 정보를 생성

- 값 검증
paid_amount, purchase, purchase['delivery_type'], purchase['purchase_list']가 들어왔는지 확인한다.
giftcard_info['type']이 존재하는지 확인한다.
type과 amount를 가지고 총 결제되야할 금액을 계산하고 프론트에서 넘어온 paid_amount가 같은지 확인한다.

- 결제 정보 merchant_uid 생성
- email, sms인지에 따라 동적으로 필드 생성

2. 결제 후 서버에서 결제완료 처리

- 값 검증
imp_uid가 존재하는지 확인

아래 검증은 모두 실패하면 환불되도록 설정

merchant_uid가 넘어왔는지 확인

user와 merchant_uid를 가지고 결제 전 정보가 존재하는지 확인

IamPort에서 결제된 금액과 결제 전 정보에서 포함된 결제 금액과 같은지 확인

핀번호를 생성
