from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import ChatMessage
import json
from datetime import datetime
from django.db.models import Q


User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_authenticated:
            # Create a unique room name for the user
            self.room_group_name = f'chat_{self.user.id}'
            
            # Join user's personal room
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            
            self.accept()
            
            # Send connection confirmation
            self.send(text_data=json.dumps({
                'type': 'connection_status',
                'status': 'connected',
                'user_id': self.user.id
            }))
        else:
            self.close()

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', '')
        
        if message_type == 'chat_message':
            receiver_id = data.get('receiver_id')
            message = data.get('message')
            
            # Save message to database
            chat_message = ChatMessage.objects.create(
                sender=self.user,
                receiver_id=receiver_id,
                message=message,
                is_delivered=True
            )
            
            # Send to sender's room
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'receiver_id': receiver_id,
                'timestamp': chat_message.timestamp.isoformat(),
                'is_delivered': True
            }))
            
            # Send to receiver's room
            async_to_sync(self.channel_layer.group_send)(
                f'chat_{receiver_id}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user.id,
                    'receiver_id': receiver_id,
                    'timestamp': chat_message.timestamp.isoformat(),
                    'is_delivered': True
                }
            )
        
        elif message_type == 'fetch_messages':
            receiver_id = data.get('receiver_id')
            messages = self.get_message_history(receiver_id)
            self.send(text_data=json.dumps({
                'type': 'chat_history',
                'messages': messages
            }))
        
        elif message_type == 'edit_message':
            message_id = data.get('message_id')
            new_message = data.get('message')
            
            # Save message to database
            chat_message = ChatMessage.objects.get(
                sender=self.user,
                id=message_id
            )
            chat_message.message = new_message
            chat_message.save()
            
            # Extract receiver_id from the chat_message
            receiver_id = chat_message.receiver_id
            
            # Send to sender's room
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': new_message,
                'sender_id': self.user.id,
                'receiver_id': receiver_id,
                'timestamp': chat_message.timestamp.isoformat(),
                'is_delivered': True
            }))
            
            # Send to receiver's room
            async_to_sync(self.channel_layer.group_send)(
                f'chat_{receiver_id}',
                {
                    'type': 'chat_message',
                    'message': new_message,
                    'sender_id': self.user.id,
                    'receiver_id': receiver_id,
                    'timestamp': chat_message.timestamp.isoformat(),
                    'is_delivered': True
                }
            )
            
        elif message_type == 'delete_message':
            message_id = data.get('message_id')
            delete_type = data.get('deleteTypeMessage')

            try:
                chat_message = ChatMessage.objects.get(id=message_id)
                receiver_id = chat_message.receiver_id

                if chat_message.sender == self.user or chat_message.receiver == self.user:
                    if delete_type == 'delete':
                        # Individual delete - mark as deleted only for the current user
                        if chat_message.sender == self.user:
                            chat_message.deleted_by_sender = True
                        else:
                            chat_message.deleted_by_receiver = True
                        chat_message.save()

                        # Prepare deletion notification only for the current user
                        deletion_data = {
                            'type': 'delete',
                            'message_id': message_id,
                            'sender_id': chat_message.sender_id,
                            'receiver_id': receiver_id,
                            'delete_type': delete_type
                        }
                        self.send(text_data=json.dumps(deletion_data))

                    elif delete_type == 'delete_all' and chat_message.sender == self.user:
                        # Delete for all - only sender can do this
                        chat_message.deleted_by_sender = True
                        chat_message.deleted_by_receiver = True
                        chat_message.save()

                        # Prepare deletion notification for both users
                        deletion_data = {
                            'type': 'delete_message',
                            'message_id': message_id,
                            'sender_id': chat_message.sender_id,
                            'receiver_id': receiver_id,
                            'delete_type': delete_type
                        }

                        # Send to both sender and receiver
                        self.send(text_data=json.dumps(deletion_data))
                        async_to_sync(self.channel_layer.group_send)(
                            f'chat_{receiver_id}',
                            {
                                'type': 'delete_message',
                                **deletion_data
                            }
                        )

                    else:
                        self.send(text_data=json.dumps({
                            'type': 'error',
                            'message': 'Invalid delete type or not authorized to delete for all'
                        }))
                else:
                    self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'You are not authorized to delete this message'
                    }))

            except ChatMessage.DoesNotExist:
                self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Message not found'
                }))
                
        elif message_type == 'clear_chat':
            receiver_id = data.get('receiver_id')
            
            try:
                # Update messages where user is sender
                ChatMessage.objects.filter(
                    sender=self.user,
                    receiver_id=receiver_id
                ).update(deleted_by_sender=True)
                
                # Update messages where user is receiver
                ChatMessage.objects.filter(
                    sender_id=receiver_id,
                    receiver=self.user
                ).update(deleted_by_receiver=True)
                
                # Prepare clear chat notification
                clear_data = {
                    'type': 'chat_cleared',
                    'sender_id': self.user.id,
                    'receiver_id': receiver_id,
                    'last_message': None
                }
                
                # Send confirmation to sender
                self.send(text_data=json.dumps(clear_data))
                
            except Exception as e:
                self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Failed to clear chat: {str(e)}'
                }))    

    def message_deleted(self, event):
        """
        Handler for message_deleted type events
        """
        self.send(text_data=json.dumps(event))

    def chat_message(self, event):
        """
        Handler for chat_message type events
        """
        self.send(text_data=json.dumps(event))

    def get_message_history(self, receiver_id):
        messages = ChatMessage.objects.filter(
            Q(sender=self.user, receiver_id=receiver_id) |
            Q(sender_id=receiver_id, receiver=self.user)
        ).order_by('timestamp')
        
        return [{
            'id': msg.id,
            'sender': {
                'id': msg.sender.id,
                'username': msg.sender.username,
                'email': msg.sender.email,
                'last_login': msg.sender.last_login.isoformat() if msg.sender.last_login else None,
                'is_active': msg.sender.is_active
            },
            'receiver': {
                'id': msg.receiver.id,
                'username': msg.receiver.username,
                'email': msg.receiver.email,
                'last_login': msg.receiver.last_login.isoformat() if msg.receiver.last_login else None,
                'is_active': msg.receiver.is_active
            },
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat(),
            'is_read': msg.is_read
        } for msg in messages]

    def delete_message(self, event):
        """
        Handler for delete_message type events
        """
        # Forward the deletion event to the WebSocket
        self.send(text_data=json.dumps(event))