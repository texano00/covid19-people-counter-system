from flask import Flask
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import random
import string
import os
import json
from db import connect, insertData

cameras = [{
    "url": "https://images2-corrierefiorentino.corriereobjects.it/methode_image/CorriereFiorentino/Video/2020/03/21/Fiorentino/Foto%20-%20Trattate/IMG-1087-kB1B--640x360@CorriereFiorentino-Web-Firenze.JPG",
    "code": "coop"
}]
engineHost = "http://engine:5000"

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def getNewFrame():
    print("getNewFrame")
    for camera in cameras:
        response = requests.get(camera['url'])
        imagePath = "/tmp/"+randomString()+".jpg"
        if response.status_code == 200:
            print("gotNewFrame")
            with open(imagePath, 'wb') as f:
                f.write(response.content)
                count = countPeople(imagePath)
                if(count!=-1):
                    saveToDb(count, camera['code'])
                os.remove(imagePath)
        else:
            print("Error retrieving a new frame")


def countPeople(imagePath):
    print("countPeople")
    threshold = 0.3
    url = engineHost + "/model/predict?threshold=0.3"
    files = {'image': open(imagePath,'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("countedPeople")
        jsonData = json.loads(response.text)
        jsonData['predictions'] = list(filter(lambda item: (item['label'] == 'person'), jsonData['predictions']))        
        # print(jsonData['predictions'])
        people = len(jsonData['predictions'])
        print(people)
        return people
    else:
        print("Error calling engine")
        return -1

def saveToDb(count, code):
    # TODO: save to postgres
    insertData(count, code)

scheduler = BackgroundScheduler()
scheduler.add_job(func=getNewFrame, trigger="interval", seconds=15)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
app = Flask(__name__)
connect()

@app.route('/ping')
def hello_world():
    return 'pong'
