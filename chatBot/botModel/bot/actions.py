import importlib
import src
import yaml


class ArgiActions():
    def __init__(self) -> None:
        self.intent_map = {}
        self.load_data()

    def load_data(self) -> None:
        # load data from yaml files
        module_path = f"{ src.__path__[0] }/bot/data"

        with open(f"{ module_path }/example_intents.yaml", "r",encoding='utf-8') as file:
            self.intent_map = yaml.safe_load(file)["intents"]

    def get(self, intent: dict):
        """
        returns ArgiActionBase
        """
        #当前仅支持单意图
        if len(intent["intents"]) > 0:
            intent_name = intent["intents"][0]
        else:
            intent_name = "fallback"

        cls_name = self.intent_map.get(intent_name).get("action")
        action_cls = getattr(
            importlib.import_module("src.bot.actions"), cls_name)
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
        module_path = f"{ src.__path__[0] }/bot/data"
        #加载农作物实体
        with open(f"{ module_path }/example_crops.yaml", "r",encoding='utf-8') as file:
            self.crops = yaml.safe_load(file)

        self.crop_names = {
            value: key for (key, value) in self.crops.items()
            }


    def _name(self, vid: str) -> str:
        if vid.startswith("crop"):
            return self.crop_names.get(vid, "unknown crop")
        else:
            return "unkonwn"

    def _vid(self, name: str) -> str:
        if name in self.crops:
            return self.crops[name]
        else:
            print(
                f"[ERROR] Something went wrong, unknown vertex name { name }")
            raise

    def _error_check(self):
        if self.error:
            return "Opps, something went wrong."


class FallbackAction(ArgiActionBase):
    def __init__(self, intent):
        super().__init__(intent)

    def execute(self, graph=None):
        """
        TBD: query some information via nbi_api in fallback case:
        https://github.com/swar/nba_api/blob/master/docs/examples/Basics.ipynb
        """
        return """
Sorry I don't understand your questions for now.
Here are supported question patterns:

学名:
    - 水稻的学名是什么?

"""
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

    def execute(self, graph) -> str:
        self._error_check()
        query = (
            "match (n{name:'"+ list(self.entity.keys())[0] +"'}) return n.sci_name"
        )
        print(
            f"[DEBUG] query for scinameAction :\n\t{ query }"
            )

        result = graph.run(query)

        return (
            f"{list(self.entity.keys())[0]}的学名是{result}"
            )
