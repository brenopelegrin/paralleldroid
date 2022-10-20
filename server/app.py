from server import db, app, api
from models import *
from resources import *
import multiprocessing

api.add_resource(CreateDevice, '/device/new')
api.add_resource(ViewDevice, '/device/<string:device_id>/view')
api.add_resource(ListAllDevices, '/device/list')

api.add_resource(CreateTask, '/task/new')
api.add_resource(ViewTask, '/task/<int:task_id>/view')
api.add_resource(ListAllTasks, '/task/list')
api.add_resource(CompleteTask, '/task/<int:task_id>/upload')

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=ListenForTasks)
    p1.start()
    app.run(debug=False, host='0.0.0.0')
