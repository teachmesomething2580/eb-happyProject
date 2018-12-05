import os
import re

import gevent
from bs4 import BeautifulSoup
from django.db import IntegrityError, transaction
from selenium.common.exceptions import NoSuchElementException

from use_point.models import UsePointCategory, UsePoint
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

        elem = driver.find_element_by_css_selector('ul.offListWrap')
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

        usepoint_dict = {
            'is_online': kwargs.get('is_online'),
            'name': kwargs.get('usepoint_name'),
            'category': c,
            'site': kwargs.get('site_url'),
        }

        if kwargs.get('img_name'):
            usepoint_dict['shop_image'] = 'images/shop_image/' + kwargs.get('img_name')

        usepoint = UsePoint.objects.get_or_create(
            **usepoint_dict,
        )

        print(usepoint)

    def handle(self, *args, **options):
        url = 'http://www.happymoney.co.kr/svc/store/offlineStore.hm'

        driver = self.get_selenium_driver()
        driver.get(url)
        item_lists = self.get_item_lists(driver)
        imgdir = self.make_dirs()

        # 이미지 이름 가져오는 re.compile
        ignorecase = re.compile(r'\w+/useStore/(.*)', re.IGNORECASE)

        thread_list = []

        for item in item_lists:
            # usePoint에 필요한 변수들
            usepoint_name = ''
            category = ''
            site_url = ''
            img_name = ''
            is_online = False

            # 이미지 다운로드
            img_url = item.select_one('img')['src']
            if img_url is not 'http://image.happymoney.co.kr/extimage/useStore/offline_noimg_book.gif':
                img_name = ignorecase.search(img_url).group(1)
                img_path = os.path.join(imgdir, img_name)
                thread_list.append(gevent.spawn(self.download_images(img_url, img_path)))

            # usePoint 정보 가져오기
            usepoint_name = item.select_one('div.info > a').get_text()
            category = (item.select_one('div.info > span').get_text() + '/').split('/')[0]
            try:
                site_url = item.select_one('span.btn > a')['href']
            except TypeError:
                site_url = ''

            try:
                self.createUsePoint(
                    usepoint_name=usepoint_name,
                    category=category,
                    is_online=is_online,
                    site_url=site_url,
                    img_name=img_name,
                )
            except IntegrityError:
                print('이미 존재하는 오프라인 몰입니다.')

        gevent.joinall(thread_list)
