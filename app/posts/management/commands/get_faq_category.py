import os

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from selenium import webdriver

from posts.models import FAQCategory, FAQSubCategory


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

        url = 'http://www.happymoney.co.kr/svc/customer/faqList.hm'
        driver = get_selenium_driver()

        driver.get(url)
        elem = driver.find_element_by_css_selector('li.cateList')
        html = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')

        divs = soup.select('div.checkWrap')[1:]

        for div in divs:
            subs = div.select('div > span.checkboxWrap')[1:]
            label = div.select_one('div > h4').getText()

            main_faq, _ = FAQCategory.objects.get_or_create(name=label)

            for sub in subs:
                sub_label = sub.select_one('label').getText()
                sub_faq, _ = FAQSubCategory.objects.get_or_create(name=sub_label, main_category=main_faq)