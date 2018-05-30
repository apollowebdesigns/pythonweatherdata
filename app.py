import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
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

def uploadNewReadings(pressure, temp, humidity):
    # A post entry.
    print('current readings are:')
    print(ref.get())

    postData = {
        'time': str(datetime.datetime.utcnow()),
        'pressure': str(pressure),
        'temperature': str(temp),
        'humidity': str(humidity)
    }

    #  Get a key for a new Post.
    newPostKey = ref.push().key

    return ref.update(postData)

@scheduler.scheduled_job('interval', seconds=10)
def runner():
    return uploadNewReadings(pressure, temp, humidity)

scheduler.start()