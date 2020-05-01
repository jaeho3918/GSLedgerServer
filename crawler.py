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
from firebase_admin import messaging

REALTIME_DB_PATH = "sYTVBn6F18VT6Ykw6L"
LASTTIME_DB_PATH = "OGn6sgTK6umHojW6QV"
REALTIME1_DB_PATH = "v6WqgKE6RLT6JkFuBv"
SHORTBUF_DB_PATH = "U6BUnY9WzFw7KZFEfg"
LONGBUF_DB_PATH = "g8fTq6WJkRcePZR8ZU"
CLOSE_REALDATA = "isY6Vg9fS6kaqi7skn6jy26"
OPEN_REALDATA = "UxO6F6BSzPkIWd6SEwqxi3n"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

URLS = {
    "AU": "https://www.investing.com/commodities/gold-historical-data",
    # https://kr.investing.com/currencies/xau-usd-historical-data
    "AG": "https://kr.investing.com/commodities/silver-historical-data",
    # https://kr.investing.com/currencies/xag-usd-historical-data
    "CUR": 'https://kr.investing.com/currencies/exchange-rates-table',
    "CNY": 'https://kr.investing.com/currencies/usd-cny-historical-data',
    "INR": 'https://kr.investing.com/currencies/usd-inr-historical-data'
}

XPATHS = {
    "AU": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()",
           "/html/body/div[5]/section/div[4]/div[2]/div/ul/li[1]/span[2]/text()"],
    "AG": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()",
           "/html/body/div[5]/section/div[4]/div[2]/div/ul/li[1]/span[2]/text()"],
    "INR": ['/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()'],
    "CUR": ["/html/body/div[5]/section/table/tbody/tr[1]/td[3]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[4]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[5]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[7]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[8]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[9]/text()"
            ],
    "CNY": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()"],
}

CUR_TABLE = ["EUR", "GBP", "JPY", "CAD", "AUD", "KRW"]

topic_limit = [False, False, False, False, False, False, False, False, False, False, False, False]

real_result = {}
last_result = {}

logging.basicConfig(filename=f'./log_Crawler.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
fileHandler = logging.FileHandler(f'./log_Crawler.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


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


def data():
    try:
        logger.info("Crawler Start")
        for key, item in URLS.items():
            rad = random.randint(33, 60)
            # rad = 8
            # print(key, rad)
            print(key, datetime.utcnow())
            time.sleep(5 + rad)
            html = requests.get(item, headers=headers).text
            xpath_data = etree.HTML(html)
            for idx, xpath in enumerate(XPATHS[key]):
                text = xpath_data.xpath(xpath)
                if key == "CUR":
                    # print(text[0].strip())
                    real_result[CUR_TABLE[idx]] = float(text[0].strip().replace(",", ""))

                elif len(key) == 2:
                    if idx == 1:
                        real_result[f"YES{key}"] = float(text[0].strip().replace(",", ""))
                    else:
                        real_result[key] = float(text[0].strip().replace(",", ""))

                else:
                    # print(float(text[0].strip().replace(",", "")))
                    real_result[key] = float(text[0].strip().replace(",", ""))
    except:
        logger.info("Crawler ERROR")

    now = datetime.utcnow()

    real_result1 = real_result.copy()

    real_result["DATE"] = datetime.utcnow().timestamp()
    print(real_result)

    now = datetime.utcnow()
    real_result1["DATE"] = f"{datetime.utcnow()}"[:-7]
    print(datetime.utcnow())
    print(real_result1["DATE"])

    try:
        last_buf = real_result.copy()
        last_buf.pop("DATE")
        last_buf.pop("YESAU")
        last_buf.pop("YESAG")
    except:
        logger.info("Crawler ERROR")

    last_date = closeTime(now)
    last_result[last_date] = last_buf
    print(last_result)

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

    logger.info("Crawler Upload")

    global topic_limit
    message(topic_limit)


def getShortChartBuf():
    limit_len = 70

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
    print(len(list_query) // limit_len)

    ag_list = []
    au_list = []
    date_list = []

    # 리스트 만들기
    for date, items in dict(list_query).items():
        date_list.append(date[0:3] + "/" + date[4:5] + "/" + date[6:7])
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

    # 제한길이 -1 까지 리스트 줄이기(마지막 날짜가 들어갈 자리확보)
    # while len(ag_list) != (limit_len - 1):
    #     print(len(ag_list))
    #     ag_list.pop(18)
    #     au_list.pop(18)
    #     date_list.pop(18)

    # #마지막 날짜의 가격 합치기
    # ag_list.append(ag_last)
    # au_list.append(au_last)
    # date_list.append(date_last)

    print(len(ag_list), ag_list[:-1])
    print(len(au_list), au_list[:-1])
    print(len(date_list), date_list[:-1])

    db.reference(f"/{SHORTBUF_DB_PATH}").set({"AU": au_list[:-1],
                                              "AG": ag_list[:-1],
                                              "DATE": date_list[:-1]
                                              })
    logger.info("Crawler Upload")


def getLongChartBuf():
    start_Date = 19920918
    limit_len = 279

    try:
        cred = credentials.Certificate(
            "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})
        print("Success Firebase Upload")
    except:
        pass

    ref = db.reference(f"/{LASTTIME_DB_PATH}").order_by_key().start_at(str(start_Date))

    list_query = ref.get()

    print('query length', len(list_query))

    # 가져온 데이터를 제한길이로 나눔
    step = len(list_query) // limit_len
    print(len(list_query) // limit_len)

    ag_list = []
    au_list = []
    date_list = []

    # 리스트 만들기
    for date, items in dict(list_query).items():
        date_list.append(date)
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

    # 제한길이 -1 까지 리스트 줄이기(마지막 날짜가 들어갈 자리확보)
    # while len(ag_list) != (limit_len - 1):
    #     print(len(ag_list))
    #     ag_list.pop(18)
    #     au_list.pop(18)
    #     date_list.pop(18)

    # #마지막 날짜의 가격 합치기
    # ag_list.append(ag_last)
    # au_list.append(au_last)
    # date_list.append(date_last)

    # print(len(ag_list),ag_list)
    # print(len(au_list),au_list)
    # print(len(date_list),date_list)

    db.reference(f"/{LONGBUF_DB_PATH}").set({"AU": au_list,
                                             "AG": ag_list,
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


def message(topic_limit):
    # See documentation on defining a message payload.
    try:
        ref = db.reference(f"/{REALTIME1_DB_PATH}").get()

        print(ref)

        title = f"Price Alert"

        price_list = [1.0, 2.0, 3.0]
        price_list = [0.1, 0.2, 0.3]

        AU = (ref['AU'] - ref['YESAU']) / ref['YESAU'] * 100
        AG = (ref['AG'] - ref['YESAG']) / ref['YESAG'] * 100

        topic_list = ["Alpha", "Beta", "Gamma"]

        for idx, price in enumerate(price_list):

            body_Slot = {}

            if AU >= price:
                if not topic_limit[idx]:
                    body_Slot['AU'] = [ref['AU'], F"▲ (+{str(AU)[:5]}%)"]
                    topic_limit[idx] = True

            elif AU <= -1 * price:
                if not topic_limit[idx + int(len(topic_limit) * 1 / 4)]:
                    body_Slot['AU'] = [ref['AU'], F"▼ ({str(AU)[:5]}%)"]
                    topic_limit[idx + int(len(topic_limit) * 1 / 4)] = True

            if AG >= price:
                if not topic_limit[idx + int(len(topic_limit) * 2 / 4)]:
                    body_Slot['AG'] = [ref['AG'], F"▲ (+{str(AG)[:5]}%)"]
                    topic_limit[idx + int(len(topic_limit) * 2 / 4)] = True

            elif AG <= -1 * price:
                if not topic_limit[idx + int(len(topic_limit) * 3 / 4)]:
                    body_Slot['AG'] = [ref['AG'], F"▼ ({str(AG)[:5]}%)"]
                    topic_limit[idx + int(len(topic_limit) * 3 / 4)] = True

            body_string = ""
            gold_buf = ""
            silver_buf = ""

            if "AU" in body_Slot.keys():
                gold_buf = f"Gold : ${body_Slot['AU'][0]}{body_Slot['AU'][1]}"

            if "AG" in body_Slot.keys():
                if "AU" in body_Slot.keys():
                    silver_buf = f", Silver : ${body_Slot['AG'][0]}{body_Slot['AG'][1]}"
                else:
                    silver_buf = f"Silver : ${body_Slot['AG'][0]}{body_Slot['AG'][1]}"

            body_string = gold_buf + silver_buf
            if body_string != "":
                # See documentation on defining a message payload.
                message = messaging.Message(
                    android=messaging.AndroidConfig(
                        ttl=timedelta(seconds=3600),
                        priority='normal',

                        notification=messaging.AndroidNotification(
                            title=title,
                            body=body_string,
                            icon='',
                            color='#fd6166',
                            sound='default'
                        ),
                    ),

                    topic=topic_list[idx]
                    # token=registration_token
                )
                # Send a message to the device corresponding to the provided
                # registration token.
                response = messaging.send(message)
                # Response is a message ID string.
                print('Successfully sent message:', topic_list[idx])
                print('global topic_limit:', topic_limit)
    except:
        print("message error")


def messageLimit():
    global topic_limit
    topic_limit = [False, False, False, False, False, False]
    print("topic_limit at ", datetime.utcnow(), "  ", topic_limit)


if __name__ == "__main__":
    # data()
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(data, 'cron', minute='*/11', hour='0-20', day_of_week='mon-fri', id="day")
    sched.add_job(data, 'cron', minute='*/11', hour='22-23', day_of_week='mon-fri', id="dayNight")
    sched.add_job(messageLimit, 'cron', minute='56', hour='21', day_of_week='mon-fri', id="reset_message_limit")
    # sched.add_job(data, 'cron', minute='*/11', day_of_week='sun', id="sunday")
    sched.add_job(data, 'cron', minute='*/11', hour='22-23', day_of_week='sun', id="sunday")

    sched.add_job(getShortChartBuf, 'cron', minute='56', hour='21', day_of_week='mon-fri', id="shortChart")
    sched.add_job(getLongChartBuf, 'cron', minute='56', hour='21', day_of_week='sat', id="longChart")

    # sched.add_job(data, 'cron', minute='0-59/11', hour='22-23', day_of_week='sun-fri', id="night")
    # sched.add_job(data, 'cron', hour='0-7', minute='*/5', second='18', day_of_week='sat', id="data_sat")
    # sched.add_job(quit_chrome_hoilday, 'cron', hour='7', minute='8', day_of_week='sat', id="holiday_quit")
    # sched.add_job(website, 'cron', day='*/1', hour='5', minute='18', id="website")

    print('scheduler start', datetime.utcnow())
    sched.start()

    while True:
        time.sleep(18)
