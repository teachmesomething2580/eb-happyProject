import datetime
import os
import re

import gevent
from django.conf import settings
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from django.db import IntegrityError
from selenium import webdriver
import requests

from event.models import Event


class Command(BaseCommand):
    def make_dirs(self):
        """
        site-images 폴더가 없다면 생성
        """
        _imgdir = os.path.join(settings.MEDIA_ROOT, 'images', 'event')

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

        ignorecase = re.compile(r'extimage/.*/.*/(.*)', re.IGNORECASE)

        imgdir = self.make_dirs()

        url = "http://www.happymoney.co.kr/svc/event/m6001L.hm?category="
        driver = get_selenium_driver()

        category_list = [1, 2, 3, 4, 5, 8, 61]
        category_names = {
            1: 'happy',
            2: 'join',
            3: 'invite',
            4: 'cashback',
            5: 'alliance',
            8: 'entry',
            61: 'comment',
        }
        thread_list = []

        for i in category_list:
            driver.get(url + str(i))

            elem = driver.find_element_by_css_selector('#tableList')
            html = elem.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            elist = soup.select('li')

            category = category_names[i]

            for e in elist:
                img_url = e.select_one('img')['src']
                img_name = ignorecase.search(img_url).group(1)
                img_path = os.path.join(imgdir, img_name)

                thread_list.append(gevent.spawn(self.download_images(img_url, img_path)))

                tag = e.select_one('span.label').getText()
                title = e.select_one('strong.name').getText()
                start, end = e.select_one('span.date').getText().split('~ ')
                start = datetime.datetime.strptime(start.split('(')[0], '%Y-%m-%d')
                end = datetime.datetime.strptime(end.split('(')[0], '%Y-%m-%d')

                try:
                    event = Event.objects.create(
                        photo='images/event/' + img_name,
                        tag=tag,
                        category=category,
                        title=title,
                        start=start,
                        end=end,
                    )
                    print(event)
                except IntegrityError:
                    print('이미 존재하는 Event')

        gevent.joinall(thread_list)
