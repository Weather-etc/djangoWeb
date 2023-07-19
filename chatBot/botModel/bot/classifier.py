import yaml
import ahocorasick
import jieba


class ArgiClassifier():
    def __init__(self) -> None:
        self.crops = {}

        self.players = {}
        self.teams = {}
        self.entity_type_map = {}
        self.intents_map = {}
        self.setup_data()

    def setup_data(self) -> None:
        self.load_entity_data()
        self.setup_entity_tree()
        self.setup_intents_map()

    def load_entity_data(self) -> None:
        # load data from yaml files
        #加载农作物实体
        with open("./chatBot/botModel/bot/data/example_crops.yaml", "r",encoding='utf-8') as file:
            self.crops = yaml.safe_load(file)

        # with open(f"{ module_path }/example_players.yaml", "r") as file:
        #     self.players = yaml.safe_load(file)
        #
        # with open(f"{ module_path }/example_teams.yaml", "r") as file:
        #     self.teams = yaml.safe_load(file)

        #加载意图
        with open("./chatBot/botModel/bot/data/example_intents.yaml", "r",encoding='utf-8') as file:
            self.intents = yaml.safe_load(file)["intents"]

    def setup_entity_tree(self) -> None:
        #实体->类别词典
        #中文需要utf编码
        self.entity_type_map.update({
            key: "crop" for key in self.crops.keys()
            })

        # self.entity_type_map.update({
        #     key: "player" for key in self.players.keys()
        #     })
        # self.entity_type_map.update({
        #     key: "team" for key in self.teams.keys()
        #     })

        self.entity_tree = ahocorasick.Automaton()
        for index, entity in enumerate(self.entity_type_map.keys()):
            self.entity_tree.add_word(entity, (index, entity))
        self.entity_tree.make_automaton()

    # 关键字->意图词典
    def setup_intents_map(self) -> None:
        for name, intent in self.intents.items():
            self.intents_map.update({
                keyword: name for keyword in intent['keywords']
                })

    # jieba分词匹配句子中的实体
    # AC自动机中文不方便
    def get_matched_entities(self, sentence: str) -> dict:
        """
        Consume a sentence to be matched with ahocorasick
        Returns a dict: {entity: entity_type}
        """
        entities_matched = []
        words = jieba.cut(sentence)
        for word in words:
            if word in self.crops.keys():
                entities_matched.append(word)
        # for item in self.entity_tree.iter(sentence):
        #     entities_matched.append(item[1][1])
        return {
            entity: self.entity_type_map[entity] for entity in entities_matched
            }

    # AC自动机匹配句子中的意图关键字，可能有多个
    def get_matched_intents(self, sentence: str) -> tuple:
        intents_matched = set()
        for word in self.intents_map.keys():
            if word in sentence:
                intents_matched.add(
                    self.intents_map[word])
        return tuple(intents_matched)

    def get(self, sentence: str) -> dict:
        """
        Classify Sentences and Fill Slots.
        This should be done by NLP, here we fake one to demostrate
        the intent Actor --> Graph DB work flow.

        sentense:
        relation:
            - What is the relationship between Yao Ming and Lakers?
            - How does Tracy McGrady and Lakers connected?
        serving:
            - Which team had Jonathon Simmons served?
        friendship:
            - Whom does Tim Duncan follow?
            - Who are Tracy McGrady's friends?

        returns:
        {
            "entities": entities,
            "intents": intents
        }
        """
        entities = self.get_matched_entities(sentence)
        intents = self.get_matched_intents(sentence)
        return {
            "entities": entities,
            "intents": intents
        }

# if __name__ == '__main__':
#     tree = ahocorasick.Automaton()