import socketio
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework_simplejwt.tokens import AccessToken

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:5173'],  # Your frontend URL
    logger=True,
    engineio_logger=True
)

socket_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='socket.io'  # Explicitly set the Socket.IO path
)
@sio.event
async def connect(sid, environ):
    try:
        token = environ.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token.payload.get('user_id')
        
        await sio.save_session(sid, {'user_id': user_id})
        await sio.enter_room(sid, f'user_{user_id}')
        
    except Exception as e:
        print(f'Connection error: {e}')
        return False

@sio.event
async def message(sid, data):
    try:
        session = await sio.get_session(sid)
        sender_id = session['user_id']
        
        message = await ChatMessage.objects.acreate(
            sender_id=sender_id,
            receiver_id=data['receiver_id'],
            message=data['message']
        )
        
        message_data = ChatMessageSerializer(message).data
        
        # Send to both sender and receiver
        await sio.emit('message', message_data, room=f'user_{sender_id}')
        await sio.emit('message', message_data, room=f'user_{data["receiver_id"]}')
        
    except Exception as e:
        print(f'Message error: {e}')
        await sio.emit('error', {'message': str(e)}, room=sid)

@sio.event
async def message_status(sid, data):
    try:
        message = await ChatMessage.objects.aget(id=data['message_id'])
        
        if data['status_type'] == 'delivered':
            message.is_delivered = True
        elif data['status_type'] == 'read':
            message.is_delivered = True
            message.is_read = True
        
        await message.asave()
        
        # Notify message sender about the status update
        await sio.emit('message_status', {
            'message_id': message.id,
            'status_type': data['status_type'],
            'is_delivered': message.is_delivered,
            'is_read': message.is_read
        }, room=f'user_{message.sender_id}')
        
    except Exception as e:
        print(f'Status update error: {e}')
        await sio.emit('error', {'message': str(e)}, room=sid)

@sio.event
async def disconnect(sid):
    session = await sio.get_session(sid)
    print(f'User {session.get("user_id")} disconnected')