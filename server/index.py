from flask import Flask, jsonify, request, Response
from flask_request_arg import request_arg
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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/listdevices')
def listdevices():
    return jsonify(devices)

@app.route('/setstatus',methods = ['POST'])
def setstatus():
    client_uuid, client_key = str(request.args['uuid']), str(request.args['key']) #only executes the code below if param uuid is provided

    if client_uuid in devices and client_key == devices[client_uuid]["key"]:
        try:
            devices[client_uuid]["status"]="online"
            update_devices(devices)
            read_devices()
            
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
