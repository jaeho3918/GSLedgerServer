from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import time
import logging
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# 운영체제에 따라 변경

chrome_option = Options()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--disable-dev-shm-usage")
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                    'geolocation': 2, 'notifications': 2,
                                                    'auto_select_certificate': 2, 'fullscreen': 2,
                                                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                    'media_stream_mic': 2, 'media_stream_camera': 2,
                                                    'protocol_handlers': 2, 'ppapi_broker': 2,
                                                    'automatic_downloads': 2, 'midi_sysex': 2,
                                                    'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop': 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement': 2, 'durable_storage': 2}}
chrome_option.add_experimental_option('prefs', prefs)
chrome_option.add_argument("start-maximized")
chrome_option.add_argument("disable-infobars")
chrome_option.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path=f'/home/ganatran68/chromedriver', chrome_options=chrome_option)

# driver.get("https://www.naver.com")

driver.get("https://gsledger-29cad.firebaseapp.com/")

element = driver.find("/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]")

with open("test.text", "w") as f:
    f.write(driver.page_source)

# for idx1, iframe1 in enumerate(frame1):
#     driver.switch_to.frame(idx1)
#     frame2 = driver.find_elements_by_tag_name("iframe")
#     for idx2, iframe2 in enumerate(frame2):
#         driver.switch_to.frame(idx2)
#         print(f"@@@{idx1}@{idx2}@@@", driver.page_source)
#         frame3 = driver.find_elements_by_tag_name("iframe")
#         for idx3, iframe3 in enumerate(frame3):
#             driver.switch_to.frame(idx3)
#             print(f"@@@{idx1}@{idx2}@{idx3}@@@", driver.page_source)
#             driver.switch_to.parent_frame()
#         driver.switch_to.parent_frame()
#     driver.switch_to.parent_frame()

driver.close()
driver.quit()


def upload():
    cred = credentials.Certificate("./gsledger-29cad-firebase-adminsdk-o5w6i-247692c0a9.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/sYTVBn2FO8VNT9Ykw90L'})
    ref = db.reference("/REAL")
    readJson = json.load('csv_data.json')
    ref.set(readJson)
    
    # if '__name__' == '__main__':
    _path = '.'  # window '.'   # linux '/home/gah/gana_server'
    # data(_path)  # crawler to homepage(inv...)
    # upload()
