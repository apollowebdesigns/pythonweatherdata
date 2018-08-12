import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
from time import sleep

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

sense = SenseHat()
sense.clear()
scheduler = BlockingScheduler()

# needs to be path to the certificate
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://userddata.firebaseio.com'
})

# Get a database reference to our blog.
ref = db.reference('test')
latest_ref = db.reference('latest')

@scheduler.scheduled_job('interval', minutes=2)
def uploadNewReadings():
    sense.clear()
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    # sense.set_rotation(270)

    # sense.show_message("Temp is %.1f C" % temp, scroll_speed=0.10, text_colour=[255, 0, 255])

    blue = (0, 0, 255)
    white = (255, 255, 255)
    yellow = (255,255,0)

    sense.set_pixel(0, 4, white)
    sense.set_pixel(7, 4, white)
    sense.set_pixel(0, 3, white)
    sense.set_pixel(7, 3, white)
    sense.set_pixel(1, 2, white)
    sense.set_pixel(6, 2, white)
    sense.set_pixel(2, 3, white)
    sense.set_pixel(5, 3, white)
    sense.set_pixel(2, 2, white)
    sense.set_pixel(5, 2, white)
    sense.set_pixel(3, 1, white)
    sense.set_pixel(4, 1, white)
    for x in range(1, 7):
        sense.set_pixel(x, 5, white)

    sense.set_pixel(1, 6, blue)
    sense.set_pixel(0, 7, blue)
    sense.set_pixel(3, 6, blue)
    sense.set_pixel(2, 7, blue)
    sense.set_pixel(5, 6, blue)
    sense.set_pixel(4, 7, blue)
    sleep(5)
    sense.clear()

    # creating the sun
    sense.set_pixel(2, 3, yellow)
    sense.set_pixel(2, 4, yellow)
    sense.set_pixel(5, 3, yellow)
    sense.set_pixel(5, 4, yellow)
    sense.set_pixel(3, 2, yellow)
    sense.set_pixel(4, 2, yellow)
    sense.set_pixel(3, 5, yellow)
    sense.set_pixel(4, 5, yellow)
    sense.set_pixel(3, 3, yellow)
    sense.set_pixel(3, 4, yellow)
    sense.set_pixel(4, 4, yellow)
    sense.set_pixel(4, 3, yellow)
    

    # send_url = 'http://freegeoip.net/json'
    # r = requests.get(send_url)
    # j = json.loads(r.text)
    # lat = j['latitude']
    # lon = j['longitude']

    # A post entry.
    print('current readings are:')
    currentDate = str(datetime.datetime.utcnow().replace(microsecond=0).isoformat())

    print('updating the ref')
    newRef = ref.child(currentDate)

    latestPostData = {
        'datetime': currentDate,
        'pressure': str(pressure),
        'temperature': str(temp),
        'humidity': str(humidity),
        'pitemperature': str(measure_temp())
    }

    postData = {
        'pressure': str(pressure),
        'temperature': str(temp),
        'humidity': str(humidity),
        'pitemperature': str(measure_temp())
    }

    #  Get a key for a new Post.
    print('now will update the data')
    latest_ref.set(latestPostData)
    return newRef.set(postData)

scheduler.start()