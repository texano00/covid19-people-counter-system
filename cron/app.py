from flask import Flask
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import random
import string
import os
import json
from db import insertData

cameras = []
engineHost = os.getenv('ENGINE_HOST')

def replaceVariables(cameras):
    '''Es. https://www.milanocam.it/Cadorna/images_archive/[YYYY][MM][DD]/YYYY][MM][DD]_[HH]0000_Cadorna_1920x1080.jpg'''
    replacedVarsCameras = []
    for camera in cameras:
        camera['url'] = camera['url'].replace("[YYYY]", time.strftime('%Y'))
        camera['url'] = camera['url'].replace("[MM]", time.strftime('%m'))
        camera['url'] = camera['url'].replace("[DD]", time.strftime('%d'))
        camera['url'] = camera['url'].replace("[HH]", time.strftime('%H'))
        camera['url'] = camera['url'].replace("[mm]", time.strftime('%M'))
        replacedVarsCameras.append(camera)
    
    return replacedVarsCameras

def readConfig(file="config.json"):
    global cameras
    with open(file, 'r') as readedFile:
        cameras = json.load(readedFile)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def getNewFrame():
    print("getNewFrame", flush=True)
    global cameras
    cameras = replaceVariables(cameras)
    for camera in cameras:
        print(camera, flush=True)
        response = requests.get(camera['url'])
        imagePath = "/tmp/"+randomString()+".jpg"
        if response.status_code == 200:
            print("gotNewFrame", flush=True)
            with open(imagePath, 'wb') as f:
                f.write(response.content)
                count = countPeople(imagePath)
                if(count!=-1):
                    saveToDb(count, camera['code'])
                os.remove(imagePath)
        else:
            print("Error retrieving a new frame", flush=True)


def countPeople(imagePath):
    print("countPeople", flush=True)
    threshold = 0.3
    url = engineHost + "/model/predict?threshold=0.3"
    files = {'image': open(imagePath,'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("countedPeople", flush=True)
        jsonData = json.loads(response.text)
        jsonData['predictions'] = list(filter(lambda item: (item['label'] == 'person'), jsonData['predictions']))        
        # print(jsonData['predictions'])
        people = len(jsonData['predictions'])
        print(people, flush=True)
        return people
    else:
        print("Error calling engine")
        return -1

def saveToDb(count, code):
    print("saveToDb", flush=True)
    insertData(count, code)

scheduler = BackgroundScheduler()
scheduler.add_job(func=getNewFrame, trigger="interval", minutes=int(os.getenv('FREQUENCE_MINUTES')))
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
app = Flask(__name__)
readConfig()

@app.route('/ping')
def hello_world():
    return 'pong'
