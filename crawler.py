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

chrome_option = Options()
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--disable-dev-shm-usage")
chrome_option.add_argument("disable-gpu")  # 가속 사용 x
chrome_option.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재

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
# URLS = {
#     "AU": "https://kr.investing.com/currencies/xau-usd",
#     "AG": "https://kr.investing.com/currencies/xag-usd"
# }
#
# XPATHS = {
#     "AU": ['//*[@id="last_last"]',
#            '//*[@id="quotes_summary_secondary_data"]/div/ul/li[1]/span[2]'],
#     "AG": ['//*[@id="last_last"]',
#            '//*[@id="quotes_summary_secondary_data"]/div/ul/li[1]/span[2]']
# }

URL = "https://goldprice.org/ko/gold-price.html"

XPATHS = {
    "AU": '//*[@id="gpxtickerLeft_price"]',
    "AG": '//*[@id="gpxtickerMiddle_price"]'
}

real_result = {}
last_result = {}

REALTIME_DB_PATH = "sYTVBn6F18VT6Ykw6L"
LASTTIME_DB_PATH = "OGn6sgTK6umHojW6QV"
REALTIME1_DB_PATH = "v6WqgKE6RLT6JkFuBv"
SHORTBUF_DB_PATH = "U6BUnY9WzFw7KZFEfg"
LONGBUF_DB_PATH = "g8fTq6WJkRcePZR8ZU"
CLOSE_REALDATA = "isY6Vg9fS6kaqi7skn6jy26"
OPEN_REALDATA = "UxO6F6BSzPkIWd6SEwqxi3n"
REALTIMESTACK_DB_PATH = "AeBuYTRW4x0B2QQQIt"
SSSHORTBUF_DB_PATH = "mkD16PiNYs63Pdle7v"

URL = 'https://apilayer.net/api/live?access_key=84737ed2a48f0373a951aeba973fe0d9&currencies=XAU,XAG,AUD,CAD,CNY,EUR,GBP,INR,JPY,KRW&source=USD&format=1'

# topic_limit = [False, False, False, False, False, False, False, False, False, False, False, False]

logging.basicConfig(filename=f'./log_Crawler.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
fileHandler = logging.FileHandler(f'./log_Crawler.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

driver = 6
real_result = {}
last_result = {}


def chrome_reboot():
    global real_result
    global last_result
    global driver

    if driver != 6:
        time.sleep(random.randint(1, 3))
        real_result = {}
        last_result = {}
        driver.close()
        driver.quit()

    driver = 6


def driver_setting18():
    global real_result
    global last_result
    global driver

    real_result = {}
    last_result = {}

    if driver != 6:
        driver.close()
        driver.quit()

    print("driver_stteing Start : ", datetime.utcnow())

    driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)


URL18 = "https://goldprice.org/ko/gold-price.html"

XPATHS18 = {
    "AU": '//*[@id="gpxtickerLeft_price"]',
    "AG": '//*[@id="gpxtickerMiddle_price"]'
}


def data18():
    global driver
    time.sleep(random.randint(66, 369))
    if driver == 6:
        driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)

    print("crawler Start : ", datetime.utcnow())
    real_result = {}
    last_result = {}
    result = {}
    tabs = driver.window_handles
    idx1 = 0

    driver.get(URL18)
    real_result["AU"] = float(driver.find_element_by_xpath(XPATHS18["AU"]).text.replace(",", ""))
    real_result["AG"] = float(driver.find_element_by_xpath(XPATHS18["AG"]).text.replace(",", ""))
    # print(result[key])

    response = requests.get(URL)
    for key, value in response.json()["quotes"].items():
        if (key[-3:] == "XAU") | (key[-3:] == "XAG"):
            # if (key[-3:] == "XAU"):
            real_result[key[-2:]] = ((1 / value) + real_result[key[-2:]]) / 2
        else:
            real_result[key[-3:]] = value

    with open('YES.csv', 'r') as f:
        rdr = csv.reader(f)
        for line in rdr:  # line[0]:XAG  line[0]: 18.18
            real_result[line[0]] = float(line[1])

    # except:
    #     logger.info("Crawler ERROR")

    now = datetime.utcnow()

    real_result1 = real_result.copy()

    real_result["DATE"] = response.json()["timestamp"]
    print("real Databse : ", datetime.utcnow().timestamp(), real_result)

    now = datetime.utcnow()
    real_result1["DATE"] = f"{datetime.utcnow()}"[:-7]
    # print(datetime.utcnow())
    # print(real_result1["DATE"])

    try:
        last_buf = real_result.copy()
        last_buf.pop("DATE")
        last_buf.pop("YESAU")
        last_buf.pop("YESAG")

    except:
        logger.info("Crawler ERROR")

    last_date = closeTime(now)
    last_result[last_date] = last_buf
    # print(last_result)

    #     # print(real_result, last_result)

    try:
        cred = credentials.Certificate(
            "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
        print("Success Firebase Upload")
    except:
        pass

    ref = db.reference(f"/{REALTIME_DB_PATH}")
    ref.update(real_result)

    ref = db.reference(f"/{REALTIME1_DB_PATH}")
    ref.update(real_result1)

    ref = db.reference(f"/{LASTTIME_DB_PATH}")
    ref.update(last_result)

    light = encrypt(real_result1)  # "open_Database"     "decrypt_Database"

    ref = db.reference(f"/{OPEN_REALDATA}")
    ref.update(light["open_Database"])

    ref = db.reference(f"/{CLOSE_REALDATA}")
    ref.update(light["decrypt_Database"])

    ref = db.reference(f"/{REALTIMESTACK_DB_PATH}")
    count = ref.get()
    # ref.update({real_result["DATE"]: real_result})
    ref.update({real_result["DATE"]: {"DATE": real_result["DATE"], "AU": real_result["AU"], "AG": real_result["AG"]}})
    if len(count) >= 70:
        ref.child(sorted(count.keys())[0]).delete()

    logger.info("Crawler Upload")

    message()

    time.sleep(random.randint(66, 111))

    driver.close()
    driver.quit()
    driver = 6


# def driver_setting():
#     global real_result
#     global last_result
#     global driver
#
#     real_result = {}
#     last_result = {}
#
#     if driver != 6:
#         driver.close()
#         driver.quit()
#
#     print("driver_stteing Start : ", datetime.utcnow())
#
#     driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)
#
#     for idx in range(2):
#         driver.execute_script('window.open("about:blank", "_blank");')
#
#     tabs = driver.window_handles
#     idx1 = 0
#     for key, value in URLS.items():
#         driver.switch_to_window(tabs[idx1])
#         driver.get(value)
#         idx1 += 1
#
# def data():
#     global driver
#     time.sleep(random.randint(1, 3))
#     if driver == 6:
#         driver = webdriver.Chrome(executable_path=CHROMDRIVER_PATH, chrome_options=chrome_option)
#         for idx in range(2):
#             driver.execute_script('window.open("about:blank", "_blank");')
#         tabs = driver.window_handles
#         idx1 = 0
#         for key, value in URLS.items():
#             driver.switch_to_window(tabs[idx1])
#             driver.get(value)
#             idx1 += 1
#
#     print("crawler Start : ", datetime.utcnow())
#     real_result = {}
#     last_result = {}
#     result = {}
#     tabs = driver.window_handles
#     idx1 = 0
#     for key, value in URLS.items():
#         driver.switch_to_window(tabs[idx1])
#         idx1 += 1
#
#         for idx, xpath in enumerate(XPATHS[key]):
#             result[key] = float(driver.find_element_by_xpath(XPATHS[key][idx]).text.replace(",", ""))
#             # print(result[key])
#
#             if len(key) == 2:
#                 if idx == 1:
#                     real_result[f"YES{key}"] = float(result[key])
#                 else:
#                     real_result[key] = float(result[key])
#
#     response = requests.get(URL)
#     for key, value in response.json()["quotes"].items():
#         if (key[-3:] == "XAU") | (key[-3:] == "XAG"):
#             real_result[key[-2:]] = ((1 / value) + real_result[key[-2:]]) / 2
#         else:
#             real_result[key[-3:]] = value
#
#     f = open('YES.csv', 'r')
#     rdr = csv.reader(f)
#     for line in rdr:
#         real_result[line[0]] = float(line[1])
#
#     # except:
#     #     logger.info("Crawler ERROR")
#
#     now = datetime.utcnow()
#
#     real_result1 = real_result.copy()
#
#     real_result["DATE"] = response.json()["timestamp"]
#     print("real Databse : ", datetime.utcnow().timestamp(), real_result)
#
#     now = datetime.utcnow()
#     real_result1["DATE"] = f"{datetime.utcnow()}"[:-7]
#     # print(datetime.utcnow())
#     # print(real_result1["DATE"])
#
#     try:
#         last_buf = real_result.copy()
#         last_buf.pop("DATE")
#         last_buf.pop("YESAU")
#         last_buf.pop("YESAG")
#
#     except:
#         logger.info("Crawler ERROR")
#
#     last_date = closeTime(now)
#     last_result[last_date] = last_buf
#     # print(last_result)
#
#     #     # print(real_result, last_result)
#
#     try:
#         cred = credentials.Certificate(
#             "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
#         firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
#         print("Success Firebase Upload")
#     except:
#         pass
#
#     ref = db.reference(f"/{REALTIME_DB_PATH}")
#     ref.update(real_result)
#
#     ref = db.reference(f"/{REALTIME1_DB_PATH}")
#     ref.update(real_result1)
#
#     ref = db.reference(f"/{LASTTIME_DB_PATH}")
#     ref.update(last_result)
#
#     light = encrypt(real_result1)  # "open_Database"     "decrypt_Database"
#
#     ref = db.reference(f"/{OPEN_REALDATA}")
#     ref.update(light["open_Database"])
#
#     ref = db.reference(f"/{CLOSE_REALDATA}")
#     ref.update(light["decrypt_Database"])
#
#     ref = db.reference(f"/{REALTIMESTACK_DB_PATH}")
#     count = ref.get()
#     ref.update({real_result["DATE"]: real_result})
#
#     if len(count) >= 70:
#         ref.child(sorted(count.keys())[0]).delete()
#
#     logger.info("Crawler Upload")
#
#     global topic_limit
#     message(topic_limit)
#
#     time.sleep(random.randint(6, 66))
#
#     driver.close()
#     driver.quit()
#     driver = 6
# def setYES():
#     global driver
#
#     print("crawler Start : ", datetime.utcnow())
#
#     result = {}
#     tabs = driver.window_handles
#     idx1 = 0
#     for key, value in URLS.items():
#         driver.switch_to_window(tabs[idx1])
#         idx1 += 1
#
#         for idx, xpath in enumerate(XPATHS[key]):
#
#             result[key] = float(driver.find_element_by_xpath(XPATHS[key][idx]).text.replace(",", ""))
#             # print(result[key])
#
#             if len(key) == 2:
#                 if idx == 1:
#                     real_result[f"YES{key}"] = float(result[key])
#
#     response = requests.get(URL)
#     f = open('YES.csv', 'w', newline='')
#     wr = csv.writer(f)
#     wr.writerow(['YESAU', 1 / response.json()["quotes"]["USDXAU"]])
#     wr.writerow(['YESAG', 1 / response.json()["quotes"]["USDXAG"]])
#     f.close()
def closeTime(now):
    closeTime_dict = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": 21,
        "minute": 0,
        "second": 0,
        "weekday": now.weekday()
    }
    # closeTime_dict[ "value"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day'] + 1}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}/{closeTime_dict['weekday']}"
    closeTime_dict[
        "stringValue"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day']}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}"
    closeTime_dict["value"] = datetime.strptime(closeTime_dict["stringValue"], '%Y/%m/%d/%H/%M/%S')

    if now >= closeTime_dict["value"]:  #
        buf_month = ""
        buf_day = ""

        if now.month < 10:
            buf_month = f"0{now.month}"
        else:
            buf_month = f"{now.month}"

        if now.day + 1 < 10:
            buf_day = f"0{now.day + 1}"
        else:
            buf_day = f"{now.day + 1}"

        return f"{now.year}{buf_month}{buf_day}"
    else:
        buf_month = ""
        buf_day = ""

        if now.month < 10:
            buf_month = f"0{now.month}"
        else:
            buf_month = f"{now.month}"

        if now.day < 10:
            buf_day = f"0{now.day}"
        else:
            buf_day = f"{now.day}"

        return f"{now.year}{buf_month}{buf_day}"


def setYES18():
    global driver

    print("crawler Start : ", datetime.utcnow())

    real_result = {}
    last_result = {}
    result = {}
    tabs = driver.window_handles
    idx1 = 0

    driver.get(URL18)
    real_result["AU"] = float(driver.find_element_by_xpath(XPATHS18["AU"]).text.replace(",", ""))
    real_result["AG"] = float(driver.find_element_by_xpath(XPATHS18["AG"]).text.replace(",", ""))
    # print(result[key])

    response = requests.get(URL)
    f = open('YES.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(['AU', 1 / response.json()["quotes"]["USDXAU"]])
    wr.writerow(['AG', 1 / response.json()["quotes"]["USDXAG"]])
    f.close()


def getShortChartBuf():
    limit_len = 70
    print("Short Chart", datetime.utcnow())
    try:
        cred = credentials.Certificate(
            "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
        print("Success Firebase Upload")
    except:
        pass

    ref = db.reference(f"/{LASTTIME_DB_PATH}").order_by_key().limit_to_last(limit_len * 2)

    list_query = ref.get()

    # print('query length', len(list_query))

    # 가져온 데이터를 제한길이로 나눔
    step = len(list_query) // limit_len
    # print(len(list_query) // limit_len)

    ag_list = []
    au_list = []
    date_list = []

    # 리스트 만들기
    for date, items in dict(list_query).items():
        date_list.append(date[0:4] + "/" + date[4:6] + "/" + date[6:8])
        au_list.append(items["AU"])
        ag_list.append(items["AG"])

    # 마지막 날짜 가져오기
    # ag_last = ag_list[:-1]
    # au_last = au_list[:-1]
    # date_last = date_list[:-1]

    # 가져온 데이터를 스텝으로 줄이기 (-1: 마지막 날짜 제외)
    ag_list = ag_list[:-1:step]
    au_list = au_list[:-1:step]
    date_list = date_list[:-1:step]

    ag_np = np.array(ag_list)
    au_np = np.array(au_list)

    au_ag_ratio = au_np / ag_np

    db.reference(f"/{SHORTBUF_DB_PATH}").set({"AU": au_list[:-1],
                                              "AG": ag_list[:-1],
                                              "RATIO": list(au_ag_ratio),
                                              "DATE": date_list[:-1]
                                              })
    logger.info("Crawler Upload")


def getSSShortChartBuf():
    limit_len = 70
    print("Short Chart", datetime.utcnow())
    try:
        cred = credentials.Certificate(
            "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
        print("Success Firebase Upload")
    except:
        pass

    ref = db.reference(f"/{LASTTIME_DB_PATH}").order_by_key().limit_to_last(limit_len * 1)

    list_query = ref.get()

    # print('query length', len(list_query))

    # 가져온 데이터를 제한길이로 나눔
    step = len(list_query) // limit_len
    # print(len(list_query) // limit_len)

    ag_list = []
    au_list = []
    date_list = []

    # 리스트 만들기
    for date, items in dict(list_query).items():
        date_list.append(date[0:4] + "/" + date[4:6] + "/" + date[6:8])
        au_list.append(items["AU"])
        ag_list.append(items["AG"])

    # 마지막 날짜 가져오기
    # ag_last = ag_list[:-1]
    # au_last = au_list[:-1]
    # date_last = date_list[:-1]

    # 가져온 데이터를 스텝으로 줄이기 (-1: 마지막 날짜 제외)
    ag_list = ag_list[:-1:step]
    au_list = au_list[:-1:step]
    date_list = date_list[:-1:step]

    ag_np = np.array(ag_list)
    au_np = np.array(au_list)

    au_ag_ratio = au_np / ag_np

    db.reference(f"/{SSSHORTBUF_DB_PATH}").set({"AU": au_list[:-1],
                                              "AG": ag_list[:-1],
                                              "RATIO": list(au_ag_ratio),
                                              "DATE": date_list[:-1]
                                              })
    logger.info("Crawler Upload")


def getLongChartBuf():
    start_Date = 19920918
    limit_len = 279

    print("Long Chart", datetime.utcnow())
    try:
        cred = credentials.Certificate(
            "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
        print("Success Firebase Upload")
    except:
        pass

    ref = db.reference(f"/{LASTTIME_DB_PATH}").order_by_key().start_at(str(start_Date))

    list_query = ref.get()

    # print('query length', len(list_query))

    # 가져온 데이터를 제한길이로 나눔
    step = len(list_query) // limit_len
    # print(len(list_query) // limit_len)

    ag_list = []
    au_list = []
    date_list = []

    # 리스트 만들기
    for date, items in dict(list_query).items():
        date_list.append(date[0:4] + "/" + date[4:6] + "/" + date[6:8])
        au_list.append(items["AU"])
        ag_list.append(items["AG"])

    # 마지막 날짜 가져오기
    # ag_last = ag_list[:-1]
    # au_last = au_list[:-1]
    # date_last = date_list[:-1]

    # 가져온 데이터를 스텝으로 줄이기 (-1: 마지막 날짜 제외)
    ag_list = ag_list[:-1:step]
    au_list = au_list[:-1:step]
    date_list = date_list[:-1:step]

    ag_np = np.array(ag_list)
    au_np = np.array(au_list)

    au_ag_ratio = au_np / ag_np

    db.reference(f"/{LONGBUF_DB_PATH}").set({"AU": au_list,
                                             "AG": ag_list,
                                             "RATIO": list(au_ag_ratio),
                                             "DATE": date_list
                                             })


def encrypt(data_input: dict):
    slot = {
        "AU": 0,
        "AG": 0,
        "AUD": 0,
        "CAD": 0,
        "CNY": 0,
        "EUR": 0,
        "GBP": 0,
        "INR": 0,
        "JPY": 0,
        "KRW": 0,
        "YESAG": 0,
        "YESAU": 0
    }
    date_slot = data_input["DATE"]
    decrypt = {}
    encrypt = {}

    for key in slot.keys():
        number6 = random.randint(1, random.randint(1, 5) ** 10)
        floatNum1 = random.randint(0, 9)
        floatNum2 = random.randint(0, 9)
        floatNum3 = random.randint(0, 9)
        floatNum4 = random.randint(0, 9)
        floatNum5 = random.randint(0, 9)

        slot[key] = float(f"{number6}.{floatNum1}{floatNum2}{floatNum3}{floatNum4}{floatNum5}")

    for key in slot.keys():
        decrypt[key] = data_input[key] / float(slot[key])

    for key in slot.keys():
        encrypt[key] = decrypt[key] * float(slot[key])
    slot["DATE"] = date_slot

    return {"open_Database": slot, "decrypt_Database": decrypt}


def message():
    print("Message Start", datetime.utcnow())

    topic_limit = []
    with open('MESSAGE_LIMIT', 'r') as f:
        rdr = csv.reader(f)
        for line in rdr:  # line[0]:XAG  line[0]: 18.18
            for value in line:
                if value.strip() == "False":
                    topic_limit.append(False)
                elif value.strip() == "True":
                    topic_limit.append(True)

    try:

        ref = db.reference(f"/{REALTIME1_DB_PATH}").get()

        # print(ref)

        title = f"Price Alert"

        price_list = [1.0, 2.0, 3.0]

        AU = (ref['AU'] - ref['YESAU']) / ref['YESAU'] * 100
        AG = (ref['AG'] - ref['YESAG']) / ref['YESAG'] * 100
        RATIO = ref['AU'] / ref['AG']

        topic_list = ["Alpha", "Beta", "Gamma"]

        for idx, price in enumerate(price_list):

            body_Slot = {}

            if AU >= price:
                if not topic_limit[idx]:
                    body_Slot['AU'] = [format(ref['AU'], '.2f'), F"▲ (+{format(AU, '.2f')}%)"]
                    topic_limit[idx] = True

            elif AU <= -1 * price:
                if not topic_limit[idx + int(len(topic_limit) * 1 / 4)]:
                    body_Slot['AU'] = [format(ref['AU'], '.2f'), F"▼ ({format(AU, '.2f')}%)"]
                    topic_limit[idx + int(len(topic_limit) * 1 / 4)] = True

            if AG >= price:
                if not topic_limit[idx + int(len(topic_limit) * 2 / 4)]:
                    body_Slot['AG'] = [format(ref['AG'], '.2f'), F"▲ (+{format(AG, '.2f')}%)"]
                    topic_limit[idx + int(len(topic_limit) * 2 / 4)] = True

            elif AG <= -1 * price:
                if not topic_limit[idx + int(len(topic_limit) * 3 / 4)]:
                    body_Slot['AG'] = [format(ref['AG'], '.2f'), F"▼ ({format(AG, '.2f')}%)"]
                    topic_limit[idx + int(len(topic_limit) * 3 / 4)] = True

            body_string = ""
            gold_buf = ""
            silver_buf = ""

            with open('MESSAGE_LIMIT', 'w') as f:
                wr = csv.writer(f)
                wr.writerow(topic_limit)

            if "AU" in body_Slot.keys():
                gold_buf = f"Gold : ${body_Slot['AU'][0]}{body_Slot['AU'][1]}"

            if "AG" in body_Slot.keys():
                if "AU" in body_Slot.keys():
                    silver_buf = f", Silver : ${body_Slot['AG'][0]}{body_Slot['AG'][1]}"
                else:
                    silver_buf = f"Silver : ${body_Slot['AG'][0]}{body_Slot['AG'][1]}"

            body_string = gold_buf + silver_buf
            if body_string != "":
                body_string = gold_buf + silver_buf + f" Gold/Silver Ratio {format(RATIO, '.2f')}"
                # See documentation on defining a message payload.
                message = messaging.Message(
                    android=messaging.AndroidConfig(
                        ttl=timedelta(seconds=3600),
                        priority='normal',

                        notification=messaging.AndroidNotification(
                            title=title,
                            body=body_string,
                            icon='',
                            color='#fd6166'
                            # sound='default'
                        ),
                    ),

                    topic=topic_list[idx]
                    # token=registration_token
                )
                # Send a message to the device corresponding to the provided
                # registration token.
                response = messaging.send(message)
                # Response is a message ID string.
                # print('Successfully sent message:', topic_list[idx])
                # print('global topic_limit:', topic_limit)
    except:
        print("message error")


def messageLimit():
    with open('MESSAGE_LIMIT', 'w') as f:
        wr = csv.writer(f)
        wr.writerow([False, False, False, False, False, False, False, False, False, False, False, False])


if __name__ == "__main__":
    # getShortChartBuf()
    # getLongChartBuf()
    # data18()
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(data18, 'cron', minute='*/10', hour='0-20', day_of_week='mon-fri', id="day")
    sched.add_job(data18, 'cron', minute='*/10', hour='22-23', day_of_week='mon-thu', id="early_start")
    sched.add_job(data18, 'cron', minute='*/10', hour='22-23', day_of_week='sun', id="sun_early_start")

    # sched.add_job(chrome_reboot, 'cron', minute='18', second='36', hour='*/3', day_of_week='mon-fri',
    #               id="chrome_reboot")

    sched.add_job(setYES18, 'cron', minute='58', hour='20', day_of_week='mon-fri', id="yes_update")
    sched.add_job(messageLimit, 'cron', minute='15', hour='22', day_of_week='mon-fri', id="reset_message_limit")

    sched.add_job(getSSShortChartBuf, 'cron', minute='24', hour='21', day_of_week='mon-fri', id="ssshortChart")
    sched.add_job(getShortChartBuf, 'cron', minute='18', hour='21', day_of_week='mon-fri', id="shortChart")
    sched.add_job(getLongChartBuf, 'cron', minute='18', hour='21', day_of_week='sat', id="longChart")

    # sched.add_job(data, 'cron', minute='0-59/11', hour='22-23', day_of_week='sun-fri', id="night")
    # sched.add_job(data, 'cron', hour='0-7', minute='*/5', second='18', day_of_week='sat', id="data_sat")
    # sched.add_job(quit_chrome_hoilday, 'cron', hour='7', minute='8', day_of_week='sat', id="holiday_quit")
    # sched.add_job(website, 'cron', day='*/1', hour='5', minute='18', id="website")

    print('scheduler start', datetime.utcnow())
    sched.start()

    while True:
        time.sleep(18)
