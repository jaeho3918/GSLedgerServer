import requests
from lxml import etree
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
import logging

REALTIME_DB_PATH = "sYTVBn6F18VT6Ykw6L"
LASTTIME_DB_PATH = "OGn6sgTK6umHojW6QV"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

URLS = {
    "AU": "https://kr.investing.com/currencies/xau-usd-historical-data",
    "AG": "https://kr.investing.com/currencies/xag-usd-historical-data",
    "CUR": 'https://kr.investing.com/currencies/exchange-rates-table',
    "CNY": 'https://kr.investing.com/currencies/usd-cny-historical-data',
    "INR": 'https://kr.investing.com/currencies/usd-inr-historical-data'
}

XPATHS = {
    "AU": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()",
           "/html/body/div[5]/section/div[4]/div[2]/div/ul/li[1]/span[2]/text()"],
    "AG": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()",
           "/html/body/div[5]/section/div[4]/div[2]/div/ul/li[1]/span[2]/text()"],
    "CUR": ["/html/body/div[5]/section/table/tbody/tr[1]/td[3]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[4]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[5]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[7]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[8]/text()",
            "/html/body/div[5]/section/table/tbody/tr[1]/td[9]/text()"
            ],
    "CNY": ["/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()"],
    "INR": ['/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]/text()']
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


def data():
    try:
        logger.info("Crawler Start")
        for key, item in URLS.items():
            html = requests.get(item, headers=headers).text
            xpath_data = etree.HTML(html)

            for idx, xpath in enumerate(XPATHS[key]):
                text = xpath_data.xpath(xpath)
                if key == "CUR":
                    print(text[0].strip())
                    real_result[CUR_TABLE[idx]] = float(text[0].strip().replace(",", ""))

                elif len(key) == 2:
                    if idx == 1:
                        real_result[f"YES{key}"] = float(text[0].strip().replace(",", ""))
                    else:
                        real_result[key] = float(text[0].strip().replace(",", ""))

                else:
                    print(float(text[0].strip().replace(",", "")))
                    real_result[key] = float(text[0].strip().replace(",", ""))
    except:
        logger.info("Crawler ERROR")

    real_result["DATE"] = datetime.datetime.now().timestamp()
    try:
        last_buf = real_result.copy()
        last_buf.pop("DATE")
        last_buf.pop("YESAU")
        last_buf.pop("YESAG")
    except:
        logger.info("Crawler ERROR")


    last_date = datetime.datetime.now().strftime('%Y%m%d')
    last_result[last_date] = last_buf

    # print(real_result, last_result)

    try:
        cred = credentials.Certificate("./gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})

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
    sched.add_job(data, 'cron', minute='*/3', day_of_week='mon-fri', id="data_week")  # second='*/21'
    sched.add_job(data, 'cron', hour='0-7', minute='*/5', second='18', day_of_week='sat', id="data_sat")
    # sched.add_job(quit_chrome_hoilday, 'cron', hour='7', minute='8', day_of_week='sat', id="holiday_quit")
    # sched.add_job(website, 'cron', day='*/1', hour='5', minute='18', id="website")
    print('scheduler start')

    while True:
        time.sleep(29)
