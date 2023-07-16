import sys; sys.path.append('../bot')
from bot.bot import ArgiBot
from py2neo import Graph


class Bot:
    def __int__(self,
                user_name='neo4j',
                user_pass='12345678',
                user_port='7474'):
        self.graph = Graph("http://localhost:{}".format(user_port),
                           auth=(user_name, user_pass), name='neo4j')

    def query(self, sentence):
        # 创建对话机器人对象
        test_bot = ArgiBot(self.graph)
        # 使用ArgiBot.query进行问答
        return test_bot.query(sentence)
