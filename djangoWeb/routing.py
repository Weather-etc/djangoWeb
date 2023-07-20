from django.urls import path
from django.urls import re_path
from chatBot import consumers
from detailsPage.consumers_detail import detailConsumer

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/detail/(?P<entity>\w+)/$', detailConsumer.as_asgi()),
]
