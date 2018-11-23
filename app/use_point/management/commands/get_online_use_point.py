import os
import re

import gevent
from bs4 import BeautifulSoup
from django.db import IntegrityError, transaction
from selenium.common.exceptions import NoSuchElementException

from use_point.models import UsePointCategory, Usage, UsePoint
from ._private import GetUsePoint


class Command(GetUsePoint):
    def get_item_lists(self, driver):
        """
        상품권 리스트를 가져옴
        """
        while True:
            try:
                btn = driver.find_element_by_css_selector('button.btnMore.js-more')
                btn.click()
            except NoSuchElementException:
                break

        elem = driver.find_element_by_css_selector('ul.imgListWrap')
        html = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        lists = soup.findChildren('li')
        return lists

    @transaction.atomic
    def createUsePoint(self, **kwargs):
        """
        Usage와 Usepoint 를 생성하는 함수
        """
        c, _ = UsePointCategory.objects.get_or_create(name=kwargs.get('category'))

        where_to_use = Usage.objects.create(
            is_fee=kwargs.get('is_fee'),
            is_import_point=kwargs.get('is_import_point'),
            month_pay_limit=kwargs.get('month_pay_limit'),
        )

        usepoint = UsePoint.objects.get_or_create(
            is_online=kwargs.get('is_online'),
            name=kwargs.get('usepoint_name'),
            category=c,
            where_to_use=where_to_use,
            site=kwargs.get('site_url'),
            shop_image='images/shop_image/'+kwargs.get('img_name'),
        )

        print(usepoint)

    def handle(self, *args, **options):
        url = 'http://www.happymoney.co.kr/svc/store/onlineStore.hm#quick'

        driver = self.get_selenium_driver()
        driver.get(url)
        item_lists = self.get_item_lists(driver)
        imgdir = self.make_dirs()

        # 이미지 이름 가져오는 re.compile
        ignorecase = re.compile(r'\w+/useStore/(.*)', re.IGNORECASE)
        # importStore URL 작성을 위해 번호를 가져옴
        regex_import_store_number = re.compile(r"'(\w+)'")

        # importStore 사이트로 이동하기위해
        import_url_front = f"http://www.happymoney.co.kr/svc/store/useStoreView.hm?useStoreInfoId="
        import_url_back = "&pageLink=store/onlineStore.hm"

        thread_list = []

        for item in item_lists:
            # usePoint에 필요한 변수들
            usepoint_name = ''
            category = ''
            site_url = ''
            img_name = ''

            # usage에 필요한 변수들
            is_online = True
            is_fee = False
            is_import_point = False
            month_pay_limit = 0

            # 이미지 다운로드
            img_url = item.select_one('img')['src']
            if img_url is 'http://image.happymoney.co.kr/extimage/useStore/offline_noimg_book.gif':
                img_name = ignorecase.search(img_url).group(1)
                img_path = os.path.join(imgdir, img_name)
                thread_list.append(gevent.spawn(self.download_images(img_url, img_path)))

            # usePoint 정보 가져오기
            usepoint_name = item.select_one('div.info > a').get_text()
            category = (item.select_one('div.info > span').get_text() + '/').split('/')[0]
            site_url = ''

            # Usage 가져오기
            is_fee = True if item.select_one('strong.ir.ico.feesIcon') else False
            is_import_point = True if item.select_one('strong.ir.ico.storeLab') else False

            # import_point일경우
            if is_import_point:
                import_store_number = regex_import_store_number.search(
                    item.select_one('div.info > a')['onclick']).group(1)
                url = import_url_front + import_store_number + import_url_back
                driver.get(url)
                month_pay_limit = driver.find_element_by_css_selector('span#paymentMonthLimit').text
                if month_pay_limit == '없음':
                    month_pay_limit = 0
                else:
                    month_pay_limit = int(''.join(list(filter(str.isdigit, month_pay_limit))))
            else:
                site_url = item.select_one('span.btn > a')['href']

            try:
                self.createUsePoint(
                    usepoint_name=usepoint_name,
                    category=category,
                    is_online=is_online,
                    site_url=site_url,
                    img_name=img_name,

                    is_fee=is_fee,
                    is_import_point=is_import_point,
                    month_pay_limit=month_pay_limit,
                )
            except IntegrityError:
                print('이미 존재하는 온라인 몰입니다.')

        gevent.joinall(thread_list)
