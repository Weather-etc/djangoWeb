import zhipuai
zhipuai.api_key = "1326b2e0baf04d47c7bf0c359868d73e.jorLZewhkLjmFGKb"

class GPTBot:
    def __init__(self) -> None:
        pass

    def query(self, sentence, entity_dict):
        response = zhipuai.model_api.sse_invoke(
            model="chatglm_6b",
            prompt=[{"role": "user", "content": sentence}],
            temperature=0.9,
            top_p=0.7,
            incremental=True
        )
        ans=''
        for event in response.events():
            if event.event == "add":
                ans+=event.data
            elif event.event == "error" or event.event == "interrupted":
                pass
            elif event.event == "finish":
                pass
            else:
                pass
        return {"entities":entity_dict, "agent":2,"content":ans}