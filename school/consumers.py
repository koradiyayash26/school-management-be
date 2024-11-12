from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Client attempting to connect")
        await self.accept()
        await self.send_json({
            'type': 'connection_established',
            'message': 'Successfully connected to WebSocket'
        })

    async def disconnect(self, close_code):
        print(f"Client disconnected with code: {close_code}")

    async def receive_json(self, content):
        print(f"Received message: {content}")
        await self.send_json({
            'type': 'echo',
            'message': f"Server received: {content}"
        })