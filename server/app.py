from flask import Flask, jsonify, request
import json

devices = {}

def read_devices():
    with open("devices.json", "r") as json_file:
        devices = json.load(json_file)
        return devices

def update_devices(devices):
    with open("devices.json", "w") as json_file:
        json.dump(devices, json_file)

devices = read_devices()
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/listdevices')
def listdevices():
    return jsonify(devices)

@app.route('/setstatus',methods = ['POST'])
def setstatus():
    client_uuid = str(request.args['uuid'])
    if client_uuid in devices:
        try:
            devices[client_uuid]["status"]="online"
            update_devices(devices)
            read_devices()
            return "device online"
        except:
            raise Exception("error when updating client status")
            return "server error"
    else:
        return "uuid not in device list"
