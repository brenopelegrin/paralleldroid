from server import db
import marshmallow as ma
from flask_marshmallow import Marshmallow

class Device(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    key = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(16), nullable=True)

    def to_json(self):
        return {"id": self.id, "key": self.key, "status": self.status}
    
    def __repr__(self):
        return f'<Device {self.id}>'
    
class DeviceSchema(ma.Schema):
    class Meta:
        fields = ("id", "key", "status")
        model = Device
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, nullable=True)
    file = db.Column(db.String(16), nullable=True)
    status = db.Column(db.String(16), nullable=True)

    def to_json(self):
        return {"id": self.id, "device_id": self.device_id, "file": self.file, "status": self.status}
    
    def __repr__(self):
        return f'<Task {self.id}>'

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "device_id", "file", "status")
        model = Task

device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
    
db.create_all()