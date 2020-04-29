import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db
from datetime import datetime, timedelta

REALTIME1_DB_PATH = "v6WqgKE6RLT6JkFuBv"

# See documentation on defining a message payload.
cred = credentials.Certificate(
    "./gsledger-29cad-firebase-adminsdk-o5w6i-639acb814a.json")  # gsledger-29cad-firebase-adminsdk-o5w6i-4213914df7.json

firebase_admin.initialize_app(cred, {'databaseURL': 'https://gsledger-29cad.firebaseio.com/'})

ref = db.reference(f"/{REALTIME1_DB_PATH}").get()

print(ref)

title = f"Price Alert"

body = ""

# price1 = 1.5

price_list = [0.05, 2.0, 2.5]

AG = (ref['AG'] - ref['YESAG']) / ref['YESAG'] * 100

AU = (ref['AU'] - ref['YESAU']) / ref['YESAU'] * 100

# title = f"Price Alert : {ref['DATE'][:16]} UTC"


body_Slot = {}

for price in price_list:
    if AU >= price:
        body_Slot['AU'] = [ref['AU'], F"(+{str(AU)[:5]}%)"]
    
    elif AU <= -1 * price:
        body_Slot['AU'] = [ref['AU'], F"({str(AU)[:5]}%)"]
    
    if AG >= price:
        body_Slot['AG'] = [ref['AG'], F"(+{str(AG)[:5]}%)"]
    
    elif AG <= -1 * price:
        body_Slot['AG'] = [ref['AG'], F"({str(AG)[:5]}%)"]

# for price in price_list:
#
#     if AU >= price:
#         body += f"Gold : {ref['AU']} (+{str(AU)[:5]}%)"
#
#     elif AU <= -1 * price:
#         body += f"Gold : {ref['AU']} ({str(AU)[:5]}%)"
#
#
#     if AG >= price:
#         if body != "":
#             body += " & "
#         body += f"Silver: {ref['AG']} (+{str(AG)[:5]}%)"
#
#     elif AG <= -1 * price:
#         if body != "":
#             body += " & "
#         body += f"Silver : {ref['AG']} ({str(AG)[:5]}%)"

# This registration token comes from the client FCM SDKs.
registration_token = []

# topics = {"KRWLIVE","EURLIVE","GBPLIVE","AUDLIVE","CADLIVE","INRLIVE","JPYLIVE","CNYLIVE"}
topic = "TEST"

# See documentation on defining a message payload.
message = messaging.Message(
    android=messaging.AndroidConfig(
        ttl=datetime.timedelta(seconds=3600),
        priority='normal',
        notification=messaging.AndroidNotification(
            title='알림인데',
            body='백그라운드 자비 좀',
            icon='',
            color='#f45342',
            sound='default'
        ),
    ),
    data={
        'score': '850',
        'time': '2:45',
    },
    webpush=messaging.WebpushConfig(
        notification=messaging.WebpushNotification(
            title='웹 알림',
            body='여긴 어떨까',
            icon='',
        ),
    ),
    topic=topic
    #token=registration_token
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)
