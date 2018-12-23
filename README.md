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

* 주문 Model 변경 (현재는 하나의 주문에 여러 사람이 있으면 여러 주문을 생성함)
* FAQ CORS
```
