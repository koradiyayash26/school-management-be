from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import json

User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Client attempting to connect")
        self.user = self.scope["user"]
        
        if self.user.is_authenticated:
            self.room_group_name = f'chat_{self.user.id}'
            
            # Join user's personal group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            await self.send_json({
                'type': 'connection_established',
                'message': 'Successfully connected to WebSocket'
            })
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        print(f"Client disconnected with code: {close_code}")
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        """Handle incoming WebSocket messages"""
        print(f"Received message: {content}")
        message_type = content.get('type', '')
        
        if message_type == 'read_messages':
            await self.handle_read_messages(content)
        elif message_type == 'new_message':
            await self.handle_new_message(content)
        elif message_type == 'typing_status':
            await self.handle_typing_status(content)
        else:
            await self.send_json({
                'type': 'echo',
                'message': f"Server received: {content}"
            })

    # Handlers for different message types
    async def handle_read_messages(self, content):
        """Handle message read status updates"""
        await self.channel_layer.group_send(
            f'chat_{content["receiver_id"]}',
            {
                'type': 'messages_read',
                'sender_id': self.user.id,
                'chat_id': content.get('chat_id')
            }
        )

    async def handle_new_message(self, content):
        """Handle new message notifications"""
        receiver_id = content.get('receiver_id')
        await self.channel_layer.group_send(
            f'chat_{receiver_id}',
            {
                'type': 'chat_message',
                'message': content.get('message'),
                'sender_id': self.user.id
            }
        )

    async def handle_typing_status(self, content):
        """Handle typing status updates"""
        receiver_id = content.get('receiver_id')
        await self.channel_layer.group_send(
            f'chat_{receiver_id}',
            {
                'type': 'typing_notification',
                'user_id': self.user.id,
                'is_typing': content.get('is_typing', False)
            }
        )

    # Message type handlers (called by channel layer)
    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        await self.send_json({
            'type': 'new_message',
            'message': event['message'],
            'sender_id': event['sender_id']
        })

    async def messages_read(self, event):
        """Send read status update to WebSocket"""
        await self.send_json({
            'type': 'messages_read',
            'sender_id': event['sender_id'],
            'chat_id': event.get('chat_id')
        })

    async def typing_notification(self, event):
        """Send typing notification to WebSocket"""
        await self.send_json({
            'type': 'typing_status',
            'user_id': event['user_id'],
            'is_typing': event['is_typing']
        })

    async def chat_cleared(self, event):
        """Send chat cleared notification to WebSocket"""
        await self.send_json({
            'type': 'chat_cleared',
            'user_id': event['user_id']
        })

    async def message_deleted(self, event):
        """Send message deleted notification to WebSocket"""
        await self.send_json({
            'type': 'message_deleted',
            'message_id': event['message_id'],
            'chat_id': event['chat_id']
        })

    async def message_edited(self, event):
        """Send message edited notification to WebSocket"""
        await self.send_json({
            'type': 'message_edited',
            'message_id': event['message_id'],
            'new_content': event['new_content'],
            'chat_id': event['chat_id']
        })

    @database_sync_to_async
    def get_user_info(self, user_id):
        """Get user information from database"""
        try:
            user = User.objects.get(id=user_id)
            return {
                'id': user.id,
                'username': user.username,
                'is_online': True  # You might want to implement proper online status tracking
            }
        except User.DoesNotExist:
            return None