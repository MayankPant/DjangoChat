from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from .models import ChatMessages, ChatRoom
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer

    async def connect(self): 
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        """ In our chat application, what we are doing is creating a group which represents a specific chatroom where when a user joins a chatroom, the consumer adds that user's channel name into the group. When a user then sends a message, that message is broadcasted to everyone within that group(chatroom). """
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept() # this is where you are accepting the websocket connection

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        message = json.loads(text_data)
        print(text_data, type(text_data))
        # sending the message to the channel layer
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                'type' : 'chat_message',
                'username' : message['username'],
                'message' : message['message'],
                'room' : message['room']
            }
        )
        await self.save_message(message['username'], message['room'], message['message'])

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        print(message, username, room)
        
        await self.send(text_data=json.dumps(
            {
                "message" : message,
                "username" : username,
                'room' : room,
            }
        ))


    @sync_to_async #this is a consumer so we need to make sure this is treated as an asynchronous message
    def save_message(self, username, roomname, message):
         user = User.objects.get(username = username)
         room = ChatRoom.objects.get(slug=roomname)

         ChatMessages.objects.create(user = user, room = room, message_content=message)

