import requests, os
from django.conf import settings
from django.core.management import BaseCommand
from selenium import webdriver


class GetUsePoint(BaseCommand):
    help = 'UsePoint 를 크롤링하는 명령어'

    def get_selenium_driver(self):
        """
        Selenium Option을 설정하고 드라이버를 리턴
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")
        DRIVER = os.path.join(settings.ROOT_DIR, '.dev', 'bin', 'chromedriver')
        fdriver = webdriver.Chrome(DRIVER, options=options)

        return fdriver

    def make_dirs(self):
        """
        site-images 폴더가 없다면 생성
        """
        _imgdir = os.path.join(settings.MEDIA_ROOT, 'images', 'shop_image')

        if not os.path.isdir(_imgdir):
            os.makedirs(_imgdir)
        return _imgdir

    def download_images(self, img_url, img_path):
        """
        이미지를 다운받는 함수
        """
        r = requests.get(img_url, stream=True)
        with open(img_path, 'wb') as f:
            f.write(r.content)