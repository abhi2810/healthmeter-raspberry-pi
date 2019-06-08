import sys

from time import sleep
import requests
import Adafruit_DHT
from pulsesenor import Pulsesensor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

# Use a service account
cred = credentials.Certificate('cred/healthmeter-b5ac6-da53f53b29bb.json')
firebase_admin.initialize_app(cred)

#read command line argument
email = str(sys.argv[1])
# print (email)

#get uid
user = auth.get_user_by_email(email)
uuid = format(user.uid)
print (uuid)

#read bmi
db = firestore.client()
users_ref = db.collection(u'user').document(uuid).collection(u'userdata').document(u'data')
doc = users_ref.get()
height = doc.get(u'height')
weight = doc.get(u'weight')
bmi = (float(weight)*10000)/(height*height)
print(bmi)

#continous data reading and uploading
count = 0
hr = 85
p = Pulsesensor()
temp = 99
def temp():
    t = Adafruit_DHT.read_retry(11,4)
    return (str(temp))
while True:
    sleep(60)


    #hr = read from sensor
    try:
        p.startAsyncBPM()
        bpm = p.BPM
     except:
        p.stopAsyncBPM
    #temp = read from sensor
    t = temp()

    
    count += 1
    if count == 30:
        count = 0
        #http call to send data to server
        url = 'https://healthmeter.herokuapp.com/pistore?temp='+str(t)+'&hr='+str(hr)+'&bmi='+str(bmi)+'&uuid='+uuid
        print (url)
        r = requests.get(url)
        print(r.content)
