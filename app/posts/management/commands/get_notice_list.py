import datetime
import os

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from selenium import webdriver

from posts.models import NoticeCategory, Notice


class Command(BaseCommand):
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

        url = 'http://www.happymoney.co.kr/svc/customer/notice.hm'
        driver = get_selenium_driver()

        driver.get(url)

        tab_name = {
            1: '새소식',
            2: '사용처',
            3: '해피쇼핑몰',
            4: '이벤트',
        }

        for i in range(1, 5):
            tab = tab_name[i]

            notice_list = driver.find_element_by_xpath(
                "//ul[contains(@class, 'tab_2') and contains(@class, 'col5') and contains(@class, 'category')]/li[contains(@class, 'tab') and contains(@class, 'js-on')]/following-sibling::li")
            notice_list.click()

            c, _ = NoticeCategory.objects.get_or_create(name=tab)

            before_page = 0
            after_page = 0

            while True:
                elem = driver.find_element_by_css_selector('.FAQListWrap_3')
                html = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')

                notice_lists = soup.select('li')
                for notice in notice_lists:
                    title = notice.select_one('strong.question > a').getText()
                    answer = str(notice.select_one('.answer > div.inAnswer'))
                    hit = int(notice.select_one('span.hit').getText())
                    date = datetime.datetime.strptime(notice.select_one('span.date').getText(), '%Y-%m-%d')

                    try:
                        n = Notice.objects.get_or_create(
                            title=title,
                            content=answer,
                            category=c,
                            created_at=date,
                            view=hit,
                        )
                        print(n)
                    except IntegrityError:
                        print('이미 존재하는 공지입니다.')

                button = driver.find_element_by_xpath('//div[@id="getListPageNavi"]/strong/following-sibling::a')
                before_page = button.get_attribute('innerHTML')
                button.click()

                if before_page == after_page:
                    break

                after_page = before_page
