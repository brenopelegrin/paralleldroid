from flask_restful import reqparse, abort, Api, Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from server import db
from models import *
from time import sleep
import werkzeug

def abort_if_device_doesnt_exist(device_id):
    exists = db.session.query(Device.id).filter_by(id=device_id).scalar() is not None
    if exists != True:
        abort(404, message="device id {} is not registered".format(device_id))

def abort_if_task_doesnt_exist(task_id):
    exists = db.session.query(Task.id).filter_by(id=task_id).scalar() is not None
    if exists != True:
        abort(404, message="task id {} is not registered".format(task_id))

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
        parser.add_argument('status', type=str, help='Cannot validate file', location='args')
        args = parser.parse_args()
        
        device_id = args['device_id']
        file = args['file']
        status = args['status']
        
        task = Task(device_id=device_id, file=file, status=status)
        
        db.session.add(task)
        db.session.commit()
        
        return {'task_id': task.id, 'device_id': device_id, 'file': file, 'message': 'task created'}
        
class ViewDevice(Resource):
    def get(self, device_id):
        abort_if_device_doesnt_exist(device_id)
        device = Device.query.get(device_id)
        return device_schema.dump(device)

class ViewTask(Resource):
    def get(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        task = Task.query.get(task_id)
        return task_schema.dump(task)
    
class ListAllDevices(Resource):
    def get(self):
        devices = Device.query.all()
        return devices_schema.dump(devices)
        
class ListAllTasks(Resource):
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

class CompleteTask(Resource):
   def post(self, task_id):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        print(f'received task {task_id} file.')
        try:
            print("saving file")
            #image_file.save(f'{task_id}.jpg')
        except:
            print("error when saving")
        return {"message": 'file uploaded'}

def RunTask(task):
    print(f'running task no {task.id}.')
    #run

def ListenForTasks():
    while 1:
        task = Task.query.filter_by(status='ready').first()
        if task != None:
            print(f'task {task.id} is ready.')
            RunTask(task)
            task.status = "running"
            db.session.commit()
            sleep(1)
        
        