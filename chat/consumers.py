"""
WebSocket consumers for real-time chat
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat functionality"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = text_data_json['receiver_id']
        
        # Save message to database
        await self.save_message(self.room_id, receiver_id, message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'sender_username': self.user.username,
            }
        )
    
    async def chat_message(self, event):
        """Receive message from room group"""
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username,
        }))
    
    @database_sync_to_async
    def save_message(self, room_id, receiver_id, content):
        """Save message to database"""
        try:
            room = ChatRoom.objects.get(id=room_id)
            receiver = User.objects.get(id=receiver_id)
            
            Message.objects.create(
                room=room,
                sender=self.user,
                receiver=receiver,
                content=content
            )
        except Exception as e:
            print(f"Error saving message: {e}")

