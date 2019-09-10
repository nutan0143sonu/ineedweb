from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from app.models import MyUser
from .models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Connect sender",self.scope['url_route']['kwargs']['sender'])
        print("Connect Receiver",self.scope['url_route']['kwargs']['receiver'])
        print("connect user applied id",self.scope['url_route']['kwargs']['applied_job_id'])
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        self.user_applied_id = self.scope['url_route']['kwargs']['applied_job_id']
        self.sender_uuid = 'chat_%s' % self.sender

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.sender_uuid,
            self.channel_name
        )

        self.accept()
        print("connected")

    def disconnect(self, close_code):
        print("disconnect sender",self.scope['url_route']['kwargs']['sender'])
        print("disconnect Receiver",self.scope['url_route']['kwargs']['receiver'])
        print("disconnect user applied id",self.scope['url_route']['kwargs']['applied_job_id'])
        async_to_sync(self.channel_layer.group_discard)(
            self.sender_uuid,
            self.channel_name
        )
        print("disconnected")

    # Receive message from WebSocket
    def receive(self, text_data):
        print("text message",text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
             self.sender_uuid,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        user_sender = MyUser.objects.get(uuid= self.sender)
        user_receiver = MyUser.objects.get(uuid=  self.receiver)
        job = UserApplyJob.objects.get(id=self.user_applied_id)
        chat = ChatModel.objects.create(
            sender=user_sender,
            receiver=user_receiver,
            accepted_applied_job=job,
            message=message
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))