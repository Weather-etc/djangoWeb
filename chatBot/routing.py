from django.urls import path
from django.urls import re_path
from chatBot import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
