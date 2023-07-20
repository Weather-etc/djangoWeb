import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .botModel.app.robot import Bot
import datetime


class ChatConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.bot = Bot()
        self.entity_name = None;
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
        entity_dic, message, _ = self.bot.query(message)

        entity = ""
        for key, _ in entity_dic.items():
            entity = entity + key + ','
        print('response: ' + message)
        print('entity: ' + entity)

        self.send(text_data=json.dumps({
            'message': f'{message}',
            'entity': entity
        }))

