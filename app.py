import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# needs to be path to the certificate
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://userddata.firebaseio.com'
})

# Get a database reference to our blog.
ref = db.reference('test')

users_ref = ref.child('users')
ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})