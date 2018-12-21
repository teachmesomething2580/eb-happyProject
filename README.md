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
