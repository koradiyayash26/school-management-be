# """
# ASGI config for conf project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# application = get_asgi_application()
import os
from django.core.asgi import get_asgi_application
from school.socket_server import socket_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

django_app = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'http':
        if scope['path'].startswith('/socket.io/'):
            await socket_app(scope, receive, send)
        else:
            await django_app(scope, receive, send)
    elif scope['type'] == 'websocket':
        await socket_app(scope, receive, send)