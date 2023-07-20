import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
import pymysql


class detailConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.cur_data = 0
        self.data = []
        self.entity_name = ""
        self.room_name = None
        self.room_group_name = None

    # websocket建立连接时执行方法
    def connect(self):
        self.room_group_name = 'botChat'
        self.entity_name = self.scope['url_route']['kwargs']['entity']
        # TODO: search mysql database
        # 连接Mysql
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password="Sg1#iIj?4.iP",
            database='qa',
            port=3306,
            charset='utf8'
        )
        cursor = conn.cursor()
        select_sql = f"SELECT ques, ans FROM QA WHERE crop = '{self.entity_name}' LIMIT 100"
        cursor.execute(select_sql)
        self.data = cursor.fetchall()
        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

        # send initial 10 msgs
        if self.cur_data < len(self.data):
            self.send(text_data=json.dumps({
                'message': self.data[self.cur_data: min(self.cur_data + 10, len(self.data))]
            }))
            self.cur_data += 10

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # TODO: send message
        # send initial 10 msgs
        if self.cur_data < len(self.data):
            self.send(text_data=json.dumps({
                'message': self.data[self.cur_data: min(self.cur_data + 10, len(self.data))]
            }))
            self.cur_data += 10
        else:
            self.disconnect(code=400)
