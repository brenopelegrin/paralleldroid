from flask import Flask, jsonify, request, Response
from flask_request_arg import request_arg
import json
import uuid
import time
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

server_url = 'http://127.0.0.1:5000'
server_info = {}

device_ip = '127.0.0.1'
device_port = '4000'
device_uuid = 'ed76fa2f-6b99-46c0-9937-c556198a5df6'
device_key = 'chave'

setstatus_endpoint = '/devices/setstatus'
getserverinfo_endpoint = '/server/info'
joinwaitlist_endpoint = '/tasks/joinwaitlist'

def join_waitlist():
    global device_uuid, device_key
    params = {"uuid": device_uuid, "key": device_key, "ip": device_ip, "port": device_port}
    response = requests.post(server_url+joinwaitlist_endpoint, params=params)
    print(response.json())

def set_status_online():
    global device_uuid, device_key
    params = {"uuid": device_uuid, "key": device_key}
    response = requests.post(server_url+setstatus_endpoint, params=params)
    print(response.json())

def get_server_info():
    global device_uuid, device_key, server_info
    params = {"uuid": device_uuid, "key": device_key}
    response = requests.get(server_url+getserverinfo_endpoint, params=params)
    print(response.json())
    server_info = response.json()

@app.route('/tasks/assign', methods=['POST'])
def get_task():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
        response={"status": "running"}
        return jsonify(response), 200
    else:
        response={"status": "not in json format"}
        return jsonify(response), 200

if __name__ == "__main__":
    get_server_info()
    set_status_online()
    join_waitlist()

    app.run(host="0.0.0.0", port="4000", debug=True)