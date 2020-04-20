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

    real_result["DATE"] = datetime.utcnow().timestamp()
    print(real_result)

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

    ref = db.reference(f"/{LASTTIME_DB_PATH}")
    ref.update(last_result)

    logger.info("Crawler Upload")


if __name__ == "__main__":
    data()
    sched = BackgroundScheduler(timezone="utc")
    sched.start()
    sched.add_job(data, 'cron', minute='0-59/11', hour='0-23', day_of_week='mon-fri', id="day")
    # sched.add_job(data, 'cron', minute='0-59/11', hour='22-23', day_of_week='sun-fri', id="night")
    # sched.add_job(data, 'cron', hour='0-7', minute='*/5', second='18', day_of_week='sat', id="data_sat")
    # sched.add_job(quit_chrome_hoilday, 'cron', hour='7', minute='8', day_of_week='sat', id="holiday_quit")
    # sched.add_job(website, 'cron', day='*/1', hour='5', minute='18', id="website")
    print('scheduler start')

    while True:
        time.sleep(18)
