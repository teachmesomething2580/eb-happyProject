#!/usr/bin/env bash

./manage.py loaddata happygiftcard.json
./manage.py loaddata rating.json
./manage.py get_event_list
./manage.py get_gift_card_type
./manage.py get_faq_category
./manage.py get_faq_list
./manage.py get_notice_list
./manage.py get_offline_use_point
./manage.py get_online_use_point
