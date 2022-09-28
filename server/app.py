from flask import Flask, jsonify, request, Response
from flask_request_arg import request_arg
import json
import uuid
import time
#uuid.uuid4()

tasks_location="./tmp/tasks.json"
devices_location="./tmp/devices.json"

device_run_endpoint="/tasks/assign"

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

    for task in tasks:
        print(tasks[task]["device"])
        if tasks[task]["device"] != "" and tasks[task]["file"] != "" and tasks[task]["status"] != "":
            print("task got to waitlist", tasks[task])
            tasks[task]["status"] = "waitlist"

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

def send_task_to_device(task_uuid: str):
    global tasks, devices
    current_task = tasks[task_uuid]
    device_uuid = current_task["device"]

    current_device = devices[device_uuid]
    device_ip = current_device["ip"]
    device_port = current_device["port"]

    device_url="http://"+device_ip

    params = current_task
    response = requests.post(device_url+device_run_endpoint, params=params)

    print(response.json())

    return response.json()

devices = read_devices()
tasks = read_tasks()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/devices/list')
def listdevices():
    global devices
    return jsonify(devices)

@app.route('/tasks/list')
def showtasks():
    global tasks
    return jsonify(tasks)

@app.route('/tasks/<string:task_uuid>/run')
def runtask(task_uuid):
    global tasks
    global devices
    if task_uuid in tasks:
        if tasks[task_uuid]["status"] == "waitlist":
            device_response = send_task_to_device(task_uuid)
            if device_response["status"] == "running":
                tasks[task_uuid]["status"] == "running"
                update_tasks()
            else:
                response = device_confirmation
                return jsonify(response), 500
        else:
            response = {"message": "task is not ready to run"}
            return jsonify(response), 500
    else:
        response = {"message": "uuid not found"}
        return jsonify(response), 200


    response = {}

    return response, 200


@app.route('/tasks/create')
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

@app.route('/tasks/<string:task_uuid>/view')
def viewtask(task_uuid):
    if task_uuid in tasks:
        response = tasks[task_uuid]
    else:
        response = {"message": "uuid not found"}
    return jsonify(response)

@app.route('/tasks/<string:task_uuid>/edit')
def edit_task(task_uuid):
    new_device = request.args.get("device_uuid", default="", type=str)
    new_name = request.args.get("name", default="", type=str)
    new_file = request.args.get("file", default="", type=str)
    response = {}
    if task_uuid in tasks:
        if new_name != "": 
            tasks[task_uuid]["name"] = new_name 
            response["name_assigned"] = "name assigned"
        if new_file != "":
            tasks[task_uuid]["file"] = new_file 
            response["file_assigned"] = "file assigned"

        if new_device in devices:
            tasks[task_uuid]["device"] = new_device
            response["device_assigned"] = "device_uuid assigned"
        else:
            response["error_device_uuid"] = "device_uuid not found"

        update_tasks()
        
    else:
        response["error_task_uuid"] = "task_uuid not found"
    
    return jsonify(response), 200

@app.route('/devices/setstatus',methods = ['POST'])
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

@app.route('/server/info',methods = ['GET'])
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

@app.route('/tasks/joinwaitlist',methods = ['POST'])
def joinwaitlist():
    global devices
    client_uuid, client_key, client_ip, client_port = str(request.args['uuid']), str(request.args['key']), str(request.args['ip']), str(request.args['port']) #only executes the code below if param uuid is provided

    if client_uuid in devices and client_key == devices[client_uuid]["key"]:
        try:
            data_return = {
                "message": "subscribed to task wait list, please wait for task"
            }
            devices[client_uuid]["ip"] = client_ip
            devices[client_uuid]["port"] = client_port
            devices[client_uuid]["status"] = "waitlist"
            update_devices()
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
