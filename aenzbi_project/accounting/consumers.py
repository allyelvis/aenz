import json
from channels.generic.websocket import WebsocketConsumer

class SyncConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        # Handle incoming data and update models
        self.send(text_data=json.dumps({
            'message': 'Data received'
        }))
