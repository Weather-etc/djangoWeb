import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .botModel.app.robot import Bot
import datetime


class ChatConsumer(WebsocketConsumer):
    def __init__(self):
        super(ChatConsumer, self).__init__()
        self.bot = Bot()
        self.room_name = None
        self.room_group_name = None

    # websocket建立连接时执行方法
    def connect(self):
        """
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        """

        # 接受所有websocket请求
        print('received')
        self.accept()

