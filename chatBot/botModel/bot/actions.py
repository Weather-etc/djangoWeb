import importlib
import yaml

PATH = "./chatBot/botModel"


class ArgiActions():
    def __init__(self) -> None:
        self.intent_map = {}
        self.load_data()

    def load_data(self) -> None:
        # load data from yaml files
        module_path = f"{ PATH }/bot/data"

        with open(f"{ module_path }/example_intents.yaml", "r",encoding='utf-8') as file:
            self.intent_map = yaml.safe_load(file)["intents"]

    def get(self, intent: dict):
        """
        returns ArgiActionBase
        学名：1作物实体 1意图
        适宜：1城市实体 1意图
        简介：1作物/品种实体 1意图
        """
        #当前bot仅支持单实体单意图
        #有实体：交给SimBot进行问题匹配
        #没实体：交给GPT
        if len(intent["intents"]) == 1 and len(intent["entities"]) == 1:
            intent_name = intent["intents"][0]
        elif len(intent["entities"]) > 0:
            intent_name = "fallback"
        else:
            intent_name = "gptfallback"

        cls_name = self.intent_map.get(intent_name).get("action")
        action_cls = getattr(
            importlib.import_module("chatBot.botModel.bot.actions"), cls_name)
        #相当于字符串当函数名
        action = action_cls(intent)
        return action


class ArgiActionBase():
    def __init__(self, intent: dict):
        """
        intent:
        {
            "entities": entities,
            "intents": intents
        }
        """
        self.load_test_data()
        self.error = False

    def load_test_data(self) -> None:
        module_path = f"{ PATH }/bot/data"
        #加载农作物实体
        with open(f"{ module_path }/example_crops.yaml", "r",encoding='utf-8') as file:
            self.crops = yaml.safe_load(file)


    def _error_check(self):
        if self.error:
            return "Opps, something went wrong."


class FallbackAction(ArgiActionBase):
    def __init__(self, intent):
        super().__init__(intent)
        self.entity = intent["entities"]

    def execute(self, graph=None):
        return {"entities": self.entity,"content":"fallback"}

class GPTFallbackAction(ArgiActionBase):
    def __init__(self, intent):
        super().__init__(intent)
        self.entity = intent["entities"]

    def execute(self, graph=None):
        return {"entities":self.entity, "content":"fallback_gpt"}


class ScinameAction(ArgiActionBase):
    """
    match (n{name:'水稻'}) return n.sci_name
    不用id查
    """
    def __init__(self, intent):
        print(f"[DEBUG] ScinameAction intent: { intent }")
        super().__init__(intent)
        try:
            #问学名时只会有一个实体
            self.entity = intent["entities"]
        except Exception:
            print(
                f"[WARN] ScinameAction entities recognition Failure "
                f"will fallback to FallbackAction, "
                f"intent: { intent }"
                )
            self.error = True

    def execute(self, graph) -> dict:
        #如果实体不是crop
        if list(self.entity.values())[0]!='crop':
            return {"entities": self.entity ,"content":"fallback"}
        self._error_check()
        query = (
            "match (n{name:'"+ list(self.entity.keys())[0] +"'}) return n.sci_name"
        )
        print(
            f"[DEBUG] query for scinameAction :\n\t{ query }"
            )

        result = graph.run(query).data()[0]['n.sci_name']

        return {"entities": self.entity,"agent": 0,"content": f"{list(self.entity.keys())[0]}的学名是{result}"}


class ProfileAction(ArgiActionBase):
    """
    match (n{name:'水稻'}) return n.profile
    """
    def __init__(self, intent):
        print(f"[DEBUG] ProfileAction intent: { intent }")
        super().__init__(intent)
        try:
            #问简介时只会有一个实体
            self.entity = intent["entities"]
        except Exception:
            print(
                f"[WARN] ProfileAction entities recognition Failure "
                f"will fallback to FallbackAction, "
                f"intent: { intent }"
                )
            self.error = True

    def execute(self, graph) -> dict:
        #如果实体不是crop/breed
        #交给GPT
        if list(self.entity.values())[0] == 'city':
            return {"entities": self.entity,"content":'fallback_gpt'}
        self._error_check()
        obj = list(self.entity.keys())[0]
        if obj in self.crops:
            query = ("match (n{name:'"+ list(self.entity.keys())[0] +"'}) return n.profile")
            result = graph.run(query).data()[0]['n.profile']
        else :
            query = ("match (n{品种名称:'"+ list(self.entity.keys())[0] +"'}) return n.全国品审会审定意见")
            result = graph.run(query).data()[0]['n.全国品审会审定意见']

        return {"entities": self.entity,"agent":0, "content":f"{result}"}


class SuitableAction(ArgiActionBase):
    """
    match (n:city{name:'德阳'})-[归属]->(m:province) return m.name
    match (n:品种)-[适宜]->(m:province{name:'新疆'}) return n.品种名称
    合成一句
    match (n:city{name:'德阳'})-[归属]->(m:province) with m as province
    match (n:品种)-[适宜]->(province) return n.品种名称
    """
    def __init__(self, intent):
        print(f"[DEBUG] SuitableAction intent: { intent }")
        super().__init__(intent)
        try:
            #只会有一个实体
            self.entity = intent["entities"]
        except Exception:
            print(
                f"[WARN] SuitableAction entities recognition Failure "
                f"will fallback to FallbackAction, "
                f"intent: { intent }"
                )
            self.error = True

    def execute(self, graph) -> dict:
        #如果实体不是city
        #交给SimBot
        if list(self.entity.values())[0] != 'city':
            return {"entities": self.entity ,"content":"fallback"}
        self._error_check()
        query = ("match (n:city{name:'" + list(self.entity.keys())[0] +  "'})-[归属]->(m:province) with m as province\
    match (n:品种)-[适宜]->(province) return n.品种名称")
        result = graph.run(query).data()
        ans = ''
        for item in result:
            value = item['n.品种名称']
            ans += value+'、'

        if len(ans) == 0:
            return {"entities": self.entity,"agent":0, "content": f"暂未收录{list(self.entity.keys())[0]}适宜种植的作物"}


        #去除最后的顿号
        ans = ans.strip('、')
        return {"entities": self.entity,"agent":0, "content":  f"{list(self.entity.keys())[0]}适宜种植的作物有：{ans}等"}
