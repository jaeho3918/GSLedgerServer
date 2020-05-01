import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db
from datetime import datetime, timedelta
import time

REALTIME1_DB_PATH = "v6WqgKE6RLT6JkFuBv"

topic_limit = [False, False, False, False, False, False, False, False, False, False, False, False]

cred = credentials.Certificate(
    "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json

firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})


def message(topic_limit):
    # See documentation on defining a message payload.
    try:
        ref = db.reference(f"/{REALTIME1_DB_PATH}").get()

        print(ref)

        title = f"Price Alert"

        price_list = [1.0, 2.0, 3.0]

        AU = (ref['AU'] - ref['YESAU']) / ref['YESAU'] * 100
        AG = (ref['AG'] - ref['YESAG']) / ref['YESAG'] * 100

        topic_list = ["Alpha", "Beta", "Gamma"]

        for idx, price in enumerate(price_list):

            body_Slot = {}

            if AU >= price:
                if not topic_limit[idx]:
                    body_Slot['AU'] = [ref['AU'], F"▲ (+{str(AU)[:5 - 1]}%)"]
                    topic_limit[idx] = True

            elif AU <= -1 * price:
                if not topic_limit[idx + int(len(topic_limit) * 1 / 4)]:
                    body_Slot['AU'] = [ref['AU'], F"▼ ({str(AU)[:5]}%)"]
                    topic_limit[idx + int(len(topic_limit) * 1 / 4)] = True

            if AG >= price:
                if not topic_limit[idx + int(len(topic_limit) * 2 / 4)]:
                    body_Slot['AG'] = [ref['AG'], F"▲ (+{str(AG)[:5 - 1]}%)"]
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


message(topic_limit)
