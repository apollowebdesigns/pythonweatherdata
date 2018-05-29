import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

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
ref.set({
    'pressure': str(pressure),
    'temperature': str(temp),
    'humidity': str(humidity)
})