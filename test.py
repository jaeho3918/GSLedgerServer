import random
import time
from datetime import datetime
from datetime import timedelta
import requests
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import time
import csv
import logging
import random
from firebase_admin import messaging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import subprocess
import os

# def closeTime(now):
#     closeTime_dict = {
#         "year": now.year,
#         "month": now.month,
#         "day": now.day,
#         "hour": 21,
#         "minute": 0,
#         "second": 0,
#         "weekday": now.weekday()
#     }
#     # closeTime_dict[ "value"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day'] + 1}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}/{closeTime_dict['weekday']}"
#     closeTime_dict[
#         "stringValue"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day']}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}"
#     closeTime_dict["value"] = datetime.strptime(closeTime_dict["stringValue"], '%Y/%m/%d/%H/%M/%S')
#     if now >= closeTime_dict["value"]: #
#         return f"{now.year}/{now.month}/{now.day+1}"
#     else:
#         return f"{now.year}/{now.month}/{now.day}"
#
#
# while 1:
#     now = f"{datetime.utcnow()}"[:-7]
#     print(now)
#     time.sleep(1)
#     # 1587651455.079182
#     # 1587651321.157737
#     # now_dict = {
#     #     "year": now.year,
#     #     "month": now.month,
#     #     "day": now.day,
#     #     "hour": now.hour,
#     #     "minute": now.minute,
#     #     "second": now.second,
#     #     "weekday": now.weekday()
#     # }
#     #
#     # now_dict["value"] = f"{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{now.second}"
#     # # now_dict["value"] = f"{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{now.second}/{now.weekday()}"
#     #
#     # tomorrowDate = datetime.strptime(now_dict["value"], '%Y/%m/%d/%H/%M/%S')
#     # addOneDay = timedelta(days=1)
#     #
#     # tomorrowDate = now + addOneDay
#     #
#     # openTime_dict = {
#     #     "year": now.year,
#     #     "month": now.month,
#     #     "day": now.day,
#     #     "hour": 22,
#     #     "minute": 0,
#     #     "second": 0,
#     #     "weekday": now.weekday(),
#     #     "value" :  now
#     # }
#     # # openTime_dict[ "value"] = f"{openTime_dict['year']}/{openTime_dict['month']}/{openTime_dict['day'] - 1}/{openTime_dict['hour']}/{openTime_dict['minute']}/{openTime_dict['second']}/{openTime_dict['weekday']}"
#     # openTime_dict["stringValue"] = f"{openTime_dict['year']}/{openTime_dict['month']}/{openTime_dict['day']}/{openTime_dict['hour']}/{openTime_dict['minute']}/{openTime_dict['second']}"
#     # openTime_dict["value"] = datetime.strptime(openTime_dict["stringValue"],'%Y/%m/%d/%H/%M/%S')
#     #
#     #
#     #
#     # closeTime_dict = {
#     #     "year": now.year,
#     #     "month": now.month,
#     #     "day": now.day,
#     #     "hour": 21,
#     #     "minute": 0,
#     #     "second": 0,
#     #     "weekday": now.weekday()
#     # }
#     # # closeTime_dict[ "value"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day'] + 1}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}/{closeTime_dict['weekday']}"
#     # closeTime_dict["stringValue"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day']}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}"
#     # closeTime_dict["value"] = datetime.strptime(closeTime_dict["stringValue"],'%Y/%m/%d/%H/%M/%S')
#     #
#     #
#     #
#     # targetTime = datetime.strptime(f"{now.year}/{now.month}/{now.day}/21/1/0", '%Y/%m/%d/%H/%M/%S')
#     #
#     # # targetTime = datetime.utcnow()
#     #
#     # print("targetTime ",now)
#     # #
#     # # print("closeTime ",closeTime_dict["value"])
#     # #
#     # # if targetTime >= closeTime_dict["value"]: #
#     # #     print(f"{now.year}/{now.month}/{now.day}  ->  {now.year}/{now.month}/{now.day+1}")
#     # # else:
#     # #     print(f"{now.year}/{now.month}/{now.day}  ->  {now.year}/{now.month}/{now.day}")
#     #
#     # # print()
#     # # print(targetTime >= closeTime_dict["value"])
#     #
#     # print(closeTime(now))
#     # time.sleep(1)
#
# data = {
#     "AG": 15.428,
#     "AU": 1723.2,
#     "AUD": 1.535,
#     "CAD": 1.3942,
#     "CNY": 7.0774,
#     "EUR": 0.9214,
#     "GBP": 0.8065,
#     "INR": 75.653,
#     "JPY": 106.48,
#     "KRW": 1218.38,
#     "YESAG": 15.171,
#     "YESAU": 1722.2,
#     "DATE":"2006/06/06 18:18:18"
# }
#
#
#
# def encrypt(data_input: dict):
#     slot = {
#         "AU": 0,
#         "AG": 0,
#         "AUD": 0,
#         "CAD": 0,
#         "CNY": 0,
#         "EUR": 0,
#         "GBP": 0,
#         "INR": 0,
#         "JPY": 0,
#         "KRW": 0,
#         "YESAG": 0,
#         "YESAU": 0
#     }
#     date_slot = data_input["DATE"]
#     decrypt = {}
#     encrypt = {}
#
#     for key in slot.keys():
#         number6 = random.randint(1, random.randint(1, 5) ** 10)
#         floatNum1 = random.randint(0, 9)
#         floatNum2 = random.randint(0, 9)
#         floatNum3 = random.randint(0, 9)
#         floatNum4 = random.randint(0, 9)
#         floatNum5 = random.randint(0, 9)
#
#         slot[key] = f"{number6}.{floatNum1}{floatNum2}{floatNum3}{floatNum4}{floatNum5}"
#
#     for key in slot.keys():
#         decrypt[key] = data_input[key] / float(slot[key])
#     decrypt["DATE"] = date_slot
#
#     for key in slot.keys():
#         encrypt[key] = decrypt[key] * float(slot[key])
#
#
#     slot["DATE"] = date_slot
#
#     print("data_input",data_input)
#
#     print("decrypt", decrypt)  # to close database   isY6Vg9fS6kaqi7skn6jy26
#
#     print("slot", slot)  # to open database -> functions     UxO6F6BSzPkIWd6SEwqxi3n
#
#     print("encrypt", encrypt)  # at phone
#
#
#     return {"open_Database": slot, "decrypt_Database": decrypt}
#
# encrypt(data)
# Regulus6MXZ6cV6VGV
# URL = 'https://xecdapi.xe.com/v1/convert_to.json/?to=USD&from=XAU,XAG&amount=1000'
#
# response = requests.get(URL)
# print(response.status_code)
# print("timestamp",datetime.fromtimestamp(response.json()["timestamp"]))
# print("data", response.json()["quotes"])
#
# result = {}
# for key, value in response.json()["quotes"].items():
#     if (key[-3:] == "XAU")|(key[-3:] == "XAG"):
#         result[key[-2:]] = 1 / value
#     else:
#         result[key[-3:]] = value
#
# print(result)

chrome_option = Options()
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--disable-dev-shm-usage")
chrome_option.add_argument("disable-gpu")  # 가속 사용 x

chrome_option.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
# prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
#                                                     'geolocation': 2, 'notifications': 2,
#                                                     'auto_select_certificate': 2, 'fullscreen': 2,
#                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
#                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
#                                                     'protocol_handlers': 2, 'ppapi_broker': 2,
#                                                     'automatic_downloads': 2, 'midi_sysex': 2,
#                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
#                                                     'metro_switch_to_desktop': 2,
#                                                     'protected_media_identifier': 2, 'app_banner': 2,
#                                                     'site_engagement': 2, 'durable_storage': 2}}
#
# chrome_option.add_experimental_option('prefs', prefs)
chrome_option.add_argument("start-maximized")
chrome_option.add_argument("disable-infobars")
chrome_option.add_argument("--disable-extensions")

# CHROMDRIVER_PATH = f'./chromedriver_win72.exe'
CHROMDRIVER_PATH = f'./chromedriver'

URL = "https://ip.pe.kr"
# URL = "https://www.investing.com"  "https://ip.pe.kr"


COUNTRY = ["us","jp","uk","ca","is","ch","fr","se","nl"]


for i in range(1000):
    select_idx = random.randint(0,len(COUNTRY)-1)
    vpn_run = subprocess.Popen(["nordvpn","connect",COUNTRY[select_idx]])
    print(vpn_run)
    vpn_run.wait(3*60)
    print(vpn_run)

    driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)

    driver.get(URL)

    print("good")

    vpn_quit = subprocess.Popen(["nordvpn","disconnect"])
    vpn_quit.wait(60)

    print("quit")

    driver.close()
    driver.quit()



# driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)
#
# driver.get(URL)