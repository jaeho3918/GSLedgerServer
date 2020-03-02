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

driver = webdriver.Chrome(executable_path=f'./chromedriver.exe', chrome_options=chrome_option)


def upload():
    cred = credentials.Certificate("./gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/sYTVBn2FO8VNT9Ykw90L'})
    ref = db.reference("/REAL")
    readJson = json.load('csv_data.json')
    ref.set(readJson)

    # if '__name__' == '__main__':
    _path = '.'  # window '.'   # linux '/home/gah/gana_server'
    # data(_path)  # crawler to homepage(inv...)
    # upload()
