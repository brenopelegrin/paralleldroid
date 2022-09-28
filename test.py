import uuid

class Task:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.device=""
        self.status="empty"
        self.json = {
            "uuid": self.uuid,
            "device": self.device,
            "status": self.status
        }

    def assign(self, device_uuid):
        self.device = device_uuid


teste = Task()
teste.assign("teste")
print(teste.uuid, teste.device, teste.status, teste.json)
