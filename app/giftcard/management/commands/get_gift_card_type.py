import os
import re

import gevent
from django.conf import settings
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from django.db import IntegrityError
from selenium import webdriver
import requests

from giftcard.models import GiftCardCategory, GiftCardType


class Command(BaseCommand):
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

    def handle(self, *args, **options):
        def get_selenium_driver():
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

        ignorecase = re.compile(r'\w+/allProduct/(.*)', re.IGNORECASE)

        imgdir = self.make_dirs()

        url = "http://www.happymoney.co.kr/svc/shopping/allianceList.hm#quick"
        driver = get_selenium_driver()
        driver.get(url)

        elem = driver.find_element_by_css_selector('#tmpl')
        html = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')

        row_list = soup.select('.bx-viewport')

        thread_list = []
        col_list = []
        for row in row_list:
            for col in row.findAll('li'):
                col_list.append(col)

        for col in col_list:
            img_tag = col.select_one('img')
            if img_tag is None:
                continue
            img_url = img_tag['src']
            img_name = ignorecase.search(img_url).group(1)
            img_path = os.path.join(imgdir, img_name)
            thread_list.append(gevent.spawn(self.download_images(img_url, img_path)))

            site_name = col.select_one('h4').getText().split(' ')[0]
            amount = int(''.join(list(filter(str.isdigit, col.select_one('strong').getText()))))

            try:
                gc = GiftCardCategory.objects.create(
                    name=site_name,
                    shop_image='images/shop_image' + img_name,
                )
            except IntegrityError:
                gc = GiftCardCategory.objects.get(name=site_name)

            print(gc)

            gt = GiftCardType.objects.create(
                amount=amount,
                category='m',
                mall_category=gc,
            )

            print(gt)

        gevent.joinall(thread_list)