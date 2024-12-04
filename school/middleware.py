from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # Get JWT token from query string
            query_string = scope.get('query_string', b'').decode()
            token = dict(param.split('=') for param in query_string.split('&')).get('token', None)

            if token:
                # Verify the token and get the user
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                scope['user'] = await database_sync_to_async(User.objects.get)(id=user_id)
            else:
                scope['user'] = AnonymousUser()
        except Exception as e:
            print(f"JWT Auth Error: {str(e)}")
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
