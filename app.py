import os
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
from time import sleep

blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255,255,0)

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

def create_cloud():
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

def create_sun():
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


    sense.set_pixel(4, 0, yellow)
    sense.set_pixel(3, 0, yellow)
    sense.set_pixel(2, 0, yellow)
    sense.set_pixel(1, 1, yellow)
    sense.set_pixel(0, 2, yellow)
    sense.set_pixel(0, 3, yellow)
    sense.set_pixel(0, 4, yellow)
    sense.set_pixel(0, 5, yellow)
    sense.set_pixel(1, 6, yellow)
    sense.set_pixel(2, 7, yellow)
    sense.set_pixel(3, 7, yellow)
    sense.set_pixel(4, 7, yellow)
    sense.set_pixel(7, 4, yellow)
    sense.set_pixel(7, 3, yellow)
    sense.set_pixel(7, 2, yellow)
    sense.set_pixel(7, 5, yellow)
    sense.set_pixel(6, 6, yellow)
    sense.set_pixel(5, 7, yellow)
    sense.set_pixel(6, 1, yellow)
    sense.set_pixel(5, 0, yellow)

    sleep(5)
    sense.clear()

@scheduler.scheduled_job('interval', minutes=2)
def uploadNewReadings():
    sense.clear()
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    # Randomly decide what image to use
    what_to_use = random.randint(1,10)

    if what_to_use < 5:
        create_cloud()
    else:
        create_sun()

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

    print('now will update the data')
    latest_ref.set(latestPostData)
    return newRef.set(postData)

scheduler.start()