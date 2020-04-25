import requests
from lxml import etree
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import time
import logging
import random

REALTIME_DB_PATH = "sYTVBn6F18VT6Ykw6L"
LASTTIME_DB_PATH = "OGn6sgTK6umHojW6QV"

LASTTIME_DB_PATH = "OGn6sgTK6umHojW6QV"

start_Date = 19920918
limit_len = 70

cred = credentials.Certificate(
    "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
print("Success Firebase Upload")

ref = db.reference(f"/{LASTTIME_DB_PATH}").order_by_key().start_at(str(start_Date))

list_query = ref.get()

#가져온 데이터를 제한길이로 나눔
step = len(list_query)//limit_len
print(len(list_query)//limit_len)

ag_list = []
au_list = []
date_list = []

#리스트 만들기
for date, items in dict(list_query).items():
    date_list.append(date)
    au_list.append(items["AU"])
    ag_list.append(items["AG"])
    
#마지막 날짜 가져오기
ag_last = ag_list[:-1]
au_last = au_list[:-1]
date_last = date_list[:-1]

#가져온 데이터를 스텝으로 줄이기 (-1: 마지막 날짜 제외)
ag_list = ag_list[:-1:step]
au_list = au_list[:-1:step]
date_list = date_list[:-1:step]

#제한길이 -1 까지 리스트 줄이기(마지막 날짜가 들어갈 자리확보)
while len(ag_list) != (limit_len-1):
    print(len(ag_list))
    ag_list.pop(18)
    au_list.pop(18)
    date_list.pop(18)
    
#마지막 날짜의 가격 합치기
ag_list.append(ag_last)
au_list.append(au_last)
date_list.append(date_last)

print(len(ag_list),ag_list)
print(len(au_list),au_list)
print(len(date_list),date_list)

