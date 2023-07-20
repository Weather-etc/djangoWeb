import yaml
import ahocorasick
import jieba

PATH = "./chatBot/botModel"

class ArgiClassifier():
    def __init__(self) -> None:
        self.crops = {}
        self.breeds = {}
        self.cities = {}

        self.entity_type_map = {}
        self.intents_map = {}
        self.setup_data()

    def setup_data(self) -> None:
        self.load_entity_data()
        self.setup_entity_tree()
        self.setup_intents_map()

    def load_entity_data(self) -> None:
        # load data from yaml files
        module_path = f"{ PATH }/bot/data"
        #加载农作物实体
        #中文需要utf编码
        with open(f"{ module_path }/example_crops.yaml", "r",encoding='utf-8') as file:
            self.crops = yaml.safe_load(file)

        with open(f"{ module_path }/example_breeds.yaml", "r",encoding='utf-8') as file:
            self.breeds = yaml.safe_load(file)

        with open(f"{module_path}/example_cities.yaml", "r", encoding='utf-8') as file:
            self.cities = yaml.safe_load(file)

        #加载意图
        with open(f"{ module_path }/example_intents.yaml", "r",encoding='utf-8') as file:
            self.intents = yaml.safe_load(file)["intents"]

    def setup_entity_tree(self) -> None:
        #实体->类别词典
        self.entity_type_map.update({
            key: "crop" for key in self.crops
            })

        self.entity_type_map.update({
            key: "breed" for key in self.breeds
            })

        self.entity_type_map.update({
            key: "city" for key in self.cities
            })

        self.entity_tree = ahocorasick.Automaton()
        for index, entity in enumerate(self.entity_type_map.keys()):
            self.entity_tree.add_word(entity, (index, entity))
        self.entity_tree.make_automaton()

    #AC自动机 关键字->意图词典
    def setup_intents_map(self) -> None:
        for name, intent in self.intents.items():
            self.intents_map.update({
                keyword: name for keyword in intent['keywords']
                })

    #jieba分词匹配句子中的实体
    #对于品种，jieba不够robust
    def get_matched_entities(self, sentence: str) -> dict:
        """
        Consume a sentence to be matched with ahocorasick
        Returns a dict: {entity: entity_type}
        """
        entities_matched = []
        # words = jieba.cut(sentence)
        # for word in words:
        #     if word in self.crops:
        #         entities_matched.append(word)
        for item in self.entity_tree.iter(sentence):
            entities_matched.append(item[1][1])
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