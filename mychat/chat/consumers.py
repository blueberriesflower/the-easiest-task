import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from asgiref.sync import sync_to_async
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'chat_message':
            message = text_data_json['message']
            user_id = text_data_json['user_id']
            user = await sync_to_async(User.objects.get)(id=user_id)
            room_name = self.room_name
            room = await sync_to_async(ChatRoom.objects.get)(name=room_name)
            await self.save_message(user, room, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username,
                    'timestamp': str(datetime.datetime.now()),
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user,
            'timestamp': timestamp,
        }))

    @sync_to_async
    def save_message(self, user, room, message):
        """
        Saves the message to the database.
        """
        Message.objects.create(user=user, room=room, content=message)
