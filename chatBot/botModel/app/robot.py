import os.path
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'chatBot\\botModel'))
sys.path.insert(1, os.path.join(os.getcwd(), 'chatBot\\botModel\\bot'))
sys.path.insert(2, os.path.join(os.getcwd(), 'chatBot\\botModel\\bot\\data'))
from bot.bot import ArgiBot
from py2neo import Graph

import argparse
parser = argparse.ArgumentParser(description='Get response from robot')
parser.add_argument('content')
arg = parser.parse_args()


class Bot:
    def __init__(self,
                user_name='neo4j',
                user_pass='12345678',
                user_port='7474'):
        self.graph = Graph("http://localhost:{}".format(user_port),
                           auth=(user_name, user_pass), name='neo4j')

    def query(self, sentence):
        # 创建对话机器人对象
        test_bot = ArgiBot(self.graph)
        # 使用ArgiBot.query进行问答
        res = test_bot.query(sentence)
        return res['entities'], res['content'], res['agent']


if __name__ == '__main__':
    bot = Bot()
    bot.query(arg['content'])
