import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json

sense = SenseHat()
sense.clear()
scheduler = BlockingScheduler()

pressure = sense.get_pressure()
temp = sense.get_temperature()
humidity = sense.get_humidity()

# needs to be path to the certificate
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://userddata.firebaseio.com'
})

# Get a database reference to our blog.
ref = db.reference('test')
# ref.set({
#     'pressure': str(pressure),
#     'temperature': str(temp),
#     'humidity': str(humidity)
# })

# ref.set([])

def uploadNewReadings(pressure, temp, humidity):
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    # A post entry.
    print('current readings are:')
    currentDate = str(datetime.datetime.utcnow().replace(microsecond=0).isoformat())

    print('updating the ref')
    newRef = ref.child(currentDate)

    postData = {
        'pressure': str(pressure),
        'temperature': str(temp),
        'humidity': str(humidity),
        'latitude': str(lat),
        'longitude': str(lon)
    }

    #  Get a key for a new Post.
    # newPostKey = ref.push().key
    print('now will update the data')
    return newRef.set(postData)

@scheduler.scheduled_job('interval', seconds=10)
def runner():
    return uploadNewReadings(pressure, temp, humidity)

scheduler.start()