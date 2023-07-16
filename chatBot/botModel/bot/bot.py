from classifier import ArgiClassifier
from actions import ArgiActions


class ArgiBot:
    def __init__(self, graph) -> None:
        self.classifier = ArgiClassifier()
        self.actions = ArgiActions()
        self.graph = graph

    def query(self, sentence):
        intent = self.classifier.get(sentence)
        action = self.actions.get(intent)
        return action.execute(self.graph)
