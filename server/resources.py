from flask_restful import reqparse, abort, Api, Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from server import db
from models import *

def abort_if_device_doesnt_exist(device_id):
    exists = db.session.query(Device.id).filter_by(id=device_id).scalar() is not None
    if exists != True:
        abort(404, message="device id {} is not registered".format(device_id))

class CreateDevice(Resource):    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, help='Cannot validate key', location='args')
        args = parser.parse_args()
        
        key = args['key']
        
        device = Device(key=key, status="nenhum")
        
        db.session.add(device)
        db.session.commit()
        
        return {'key': key, 'message': 'device added'}
    
class CreateTask(Resource):    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('device_id', type=int, help='Cannot validate device_id', location='args')
        parser.add_argument('file', type=str, help='Cannot validate file', location='args')
        args = parser.parse_args()
        
        device_id = args['device_id']
        file = args['file']
        
        task = Task(device_id=device_id, file=file, status="nenhum")
        
        db.session.add(task)
        db.session.commit()
        
        return {'task_id': task.id, 'device_id': device_id, 'file': file, 'message': 'task created'}
        
class ViewDevice(Resource):
    def get(self, device_id):
        abort_if_device_doesnt_exist(device_id)
        device = Device.query.get(device_id)
        return device_schema.dump(device)
    
class ListAllDevices(Resource):
    def get(self):
        devices = Device.query.all()
        return devices_schema.dump(devices)
        
class ListAllTasks(Resource):
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)
        
        