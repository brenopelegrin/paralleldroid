from flask import Flask, jsonify, request, Response
from flask_request_arg import request_arg
import json
import uuid
import time
#uuid.uuid4()

tasks_location="/tmp/tasks.json"
devices_location="/tmp/devices.json"
devices = {}

class Task:
    def __init__(self, uuid=str(uuid.uuid4()), name="", device="", status="", file=""):
        self.name = name
        self.uuid = uuid
        self.file = file
        self.device = device
        self.status = status

    @property
    def createdts(self):
        return(time.time())

    def body(self):
        body = {
            "uuid4": self.uuid,
            "uuid4_hex": uuid.UUID(self.uuid).hex,
            "name": self.name,
            "device": self.device,
            "status": self.status,
            "file": self.file,
            "createdts": self.createdts
        }
        return(body)

def read_tasks():
    with open(tasks_location, "r") as json_file:
        tasks = json.load(json_file)
        return tasks

def update_tasks():
    global tasks
    with open(tasks_location, "w") as json_file:
        json.dump(tasks, json_file)

def read_devices():
    with open(devices_location, "r") as json_file:
        devices = json.load(json_file)
        return devices

def update_devices():
    global devices
    with open(devices_location, "w") as json_file:
        json.dump(devices, json_file)

devices = read_devices()
tasks = read_tasks()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/listdevices')
def listdevices():
    global devices
    return jsonify(devices)

@app.route('/showtasks')
def showtasks():
    global tasks
    return jsonify(tasks)

@app.route('/newtask')
def newtask():
    global devices, tasks
    task_uuid, task_name, task_device, task_file = request.args.get('uuid', default=None, type=str), request.args.get('name', default=None, type=str), request.args.get('device', default=None, type=str), request.args.get('file', default=None, type=str)
    newtask = Task()
    if task_name is not None:
        newtask.name = task_name
    if task_device in devices:
        newtask.device = task_device
    if task_uuid is not None:
        newtask.uuid = task_uuid

    print(newtask.body())
    tasks[newtask.uuid] = newtask.body()
    update_tasks()
    return jsonify(tasks[newtask.uuid]), 200

@app.route('/setstatus',methods = ['POST'])
def setstatus():
    global devices
    client_uuid, client_key = str(request.args['uuid']), str(request.args['key']) #only executes the code below if param uuid is provided

    if client_uuid in devices and client_key == devices[client_uuid]["key"]:
        try:
            devices[client_uuid]["status"]="online"
            update_devices()
            
            data_return = {
                "message": "status changed to online"
            }
            return jsonify(data_return), 200

        except:
            data_return = {
                "message": "server error"
            }

            raise Exception("error when updating client status")
            return jsonify(data_return), 500
    else:
        data_return = {
            "message": "uuid not in trusted devices list or invalid key"
        }
        return jsonify(data_return), 403

@app.route('/getserverinfo',methods = ['GET'])
def getserverinfo():
    global devices
    client_uuid, client_key = str(request.args['uuid']), str(request.args['key']) #only executes the code below if param uuid is provided
    server_key="teste"
    server_new_ip="0.0.0.0"
    server_new_port="5000"

    if client_uuid in devices and client_key == devices[client_uuid]["key"]:
        try:
            data_return = {
                "new_ip": server_new_ip,
                "new_port": server_new_port,
                "key": server_key,
            }
            return jsonify(data_return), 200

        except:
            data_return = {
                "message": "server error"
            }

            raise Exception("error when sending server info to client")
            return jsonify(data_return), 500
    else:
        data_return = {
            "message": "uuid not in trusted devices list or invalid key"
        }
        return jsonify(data_return), 403

@app.route('/subscribe',methods = ['POST'])
def subscribe():
    global devices
    client_uuid, client_key, client_ip, client_port = str(request.args['uuid']), str(request.args['key']), str(request.args['ip']), str(request.args['port']) #only executes the code below if param uuid is provided

    if client_uuid in devices and client_key == devices[client_uuid]["key"]:
        try:
            data_return = {
                "message": "subscribed to task wait list, please wait for task"
            }
            return jsonify(data_return), 200

        except:
            data_return = {
                "message": "server error"
            }

            raise Exception("error when sending server message to client")
            return jsonify(data_return), 500
    else:
        data_return = {
            "message": "uuid not in trusted devices list or invalid key"
        }
        return jsonify(data_return), 403
