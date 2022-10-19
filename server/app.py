from server import db, app, api
from models import *
from resources import *
import asyncio

api.add_resource(CreateDevice, '/device/new')

api.add_resource(ViewDevice, '/device/<string:device_id>/view')

api.add_resource(ListAllDevices, '/device/list')

api.add_resource(CreateTask, '/task/new')

api.add_resource(ListAllTasks, '/task/list')

if __name__ == '__main__':
    app.run(debug=True)