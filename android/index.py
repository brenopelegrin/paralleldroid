from flask import Flask, jsonify, request, Response
from flask_request_arg import request_arg
import json
import uuid
import time
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

server_info = {}

device_ip = '127.0.0.1'
device_port = '4000'
device_uuid = 'ed76fa2f-6b99-46c0-9937-c556198a5df6'
device_key = 'chave'

def join_server_waitlist():
    return None

def get_server_info():
    return None

@app.route('/receive/task', methods=['POST'])
def get_task_from_server():
    return None

if __name__ == "__main__":

    app.run(host="0.0.0.0", port="4000", debug=True)