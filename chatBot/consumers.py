import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .botModel.app.robot import Bot
import datetime


class ChatConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.bot = Bot()
        self.room_name = None
        self.room_group_name = None

    # websocket建立连接时执行方法
    def connect(self):
        self.room_group_name = 'botChat'

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = self.bot.query(message)
        print('response: ' + message)

        # 发送消息到频道组，频道组调用chat_message方法
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'{message}'
        }))
