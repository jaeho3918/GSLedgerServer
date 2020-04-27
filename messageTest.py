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

title = ""
body = ""

AG = (ref["AG"] - ref["YESAG"]) / ref["YESAG"] * 100

AU = (ref["AU"] - ref["YESAU"]) / ref["YESAU"] * 100

title = f"AG & AU Price time{ref['DATE'][:16]}"
body = f"{AG} & {AU}"


# This registration token comes from the client FCM SDKs.
# registration_token = 'ANDROID_CLIENT_TOKEN'

topic = 'TEST'
# See documentation on defining a message payload.
message = messaging.Message(
    android=messaging.AndroidConfig(
        ttl=timedelta(seconds=3600),
        priority='normal',
        notification=messaging.AndroidNotification(
            title=title,
            body=body,
            icon='',
            color='#f45342',
            sound='default'
        ),
    ),
    data={
        'score': '850',
        'time': '2:45',
    },
    topic=topic
    # token=registration_token
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)
