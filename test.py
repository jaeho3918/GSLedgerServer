import random
import time
from datetime import datetime
from datetime import timedelta

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
    if now >= closeTime_dict["value"]: #
        return f"{now.year}/{now.month}/{now.day+1}"
    else:
        return f"{now.year}/{now.month}/{now.day}"


while 1:
    now = f"{datetime.utcnow()}"[:-7]
    print(now)
    time.sleep(1)
    # 1587651455.079182
    # 1587651321.157737
    # now_dict = {
    #     "year": now.year,
    #     "month": now.month,
    #     "day": now.day,
    #     "hour": now.hour,
    #     "minute": now.minute,
    #     "second": now.second,
    #     "weekday": now.weekday()
    # }
    #
    # now_dict["value"] = f"{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{now.second}"
    # # now_dict["value"] = f"{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{now.second}/{now.weekday()}"
    #
    # tomorrowDate = datetime.strptime(now_dict["value"], '%Y/%m/%d/%H/%M/%S')
    # addOneDay = timedelta(days=1)
    #
    # tomorrowDate = now + addOneDay
    #
    # openTime_dict = {
    #     "year": now.year,
    #     "month": now.month,
    #     "day": now.day,
    #     "hour": 22,
    #     "minute": 0,
    #     "second": 0,
    #     "weekday": now.weekday(),
    #     "value" :  now
    # }
    # # openTime_dict[ "value"] = f"{openTime_dict['year']}/{openTime_dict['month']}/{openTime_dict['day'] - 1}/{openTime_dict['hour']}/{openTime_dict['minute']}/{openTime_dict['second']}/{openTime_dict['weekday']}"
    # openTime_dict["stringValue"] = f"{openTime_dict['year']}/{openTime_dict['month']}/{openTime_dict['day']}/{openTime_dict['hour']}/{openTime_dict['minute']}/{openTime_dict['second']}"
    # openTime_dict["value"] = datetime.strptime(openTime_dict["stringValue"],'%Y/%m/%d/%H/%M/%S')
    #
    #
    #
    # closeTime_dict = {
    #     "year": now.year,
    #     "month": now.month,
    #     "day": now.day,
    #     "hour": 21,
    #     "minute": 0,
    #     "second": 0,
    #     "weekday": now.weekday()
    # }
    # # closeTime_dict[ "value"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day'] + 1}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}/{closeTime_dict['weekday']}"
    # closeTime_dict["stringValue"] = f"{closeTime_dict['year']}/{closeTime_dict['month']}/{closeTime_dict['day']}/{closeTime_dict['hour']}/{closeTime_dict['minute']}/{closeTime_dict['second']}"
    # closeTime_dict["value"] = datetime.strptime(closeTime_dict["stringValue"],'%Y/%m/%d/%H/%M/%S')
    #
    #
    #
    # targetTime = datetime.strptime(f"{now.year}/{now.month}/{now.day}/21/1/0", '%Y/%m/%d/%H/%M/%S')
    #
    # # targetTime = datetime.utcnow()
    #
    # print("targetTime ",now)
    # #
    # # print("closeTime ",closeTime_dict["value"])
    # #
    # # if targetTime >= closeTime_dict["value"]: #
    # #     print(f"{now.year}/{now.month}/{now.day}  ->  {now.year}/{now.month}/{now.day+1}")
    # # else:
    # #     print(f"{now.year}/{now.month}/{now.day}  ->  {now.year}/{now.month}/{now.day}")
    #
    # # print()
    # # print(targetTime >= closeTime_dict["value"])
    #
    # print(closeTime(now))
    # time.sleep(1)




