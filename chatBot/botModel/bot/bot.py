import sys
sys.path.append('')
from classifier import ArgiClassifier
from actions import ArgiActions
from simBot.bot import SimBot
from GPTBot.bot import GPTBot


class ArgiBot:
    def __init__(self, graph) -> None:
        self.classifier = ArgiClassifier()
        self.actions = ArgiActions()
        self.graph = graph
        self.sbot = SimBot()
        self.gbot = GPTBot()

    def query(self, sentence):
        '''
        :param sentence:
        :return: dict {"agent": ,"entities": ,"content": }
        '''
        intent = self.classifier.get(sentence)
        action = self.actions.get(intent)
        ans = action.execute(self.graph)
        #如果直接匹配失败，使用Sim机器人
        if ans["content"] == 'fallback':
            ans = self.sbot.query(sentence, ans["entities"])
        #如果找不到相似问题，交给GPT
        if ans["content"] == 'fallback_gpt':
            ans = self.gbot.query(sentence, ans["entities"])
        return ans


