import os

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management import BaseCommand
from selenium import webdriver

from posts.models import FAQ, FAQSubCategory


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

        url = 'http://www.happymoney.co.kr/svc/customer/faqList.hm#quick'
        driver = get_selenium_driver()

        driver.get(url)

        before_page = 0
        after_page = 0

        while True:
            elem = driver.find_element_by_css_selector('ul.FAQList.js-faq')
            html = elem.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            faq_lists = soup.select('li')
            for faq in faq_lists:
                category = faq.select_one('span.cate').getText()
                title = faq.select_one('strong.question > a').getText()
                answer = str(faq.select_one('.answer > div.inAnswer'))

                category = FAQSubCategory.objects.get(name=category)

                faq = FAQ.objects.get_or_create(
                    category=category,
                    title=title,
                    content=answer,
                )

                print(faq)

            button = driver.find_element_by_xpath('//div[@id="getListPageNavi"]/strong/following-sibling::a')
            before_page = button.get_attribute('innerHTML')
            button.click()

            if before_page == after_page:
                break

            after_page = before_page
