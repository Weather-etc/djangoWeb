# # pip install zhipuai 请先在终端进行安装
# import zhipuai
#
# zhipuai.api_key = "1326b2e0baf04d47c7bf0c359868d73e.jorLZewhkLjmFGKb"
# response = zhipuai.model_api.sse_invoke(
# model="chatglm_6b",
# prompt= [{"role":"user","content":"推荐下性价比高的笔记本电脑"}],
# temperature= 0.9,
# top_p= 0.7,
# incremental=True
# )
#
#
# if __name__ == "__main__":
#     ans=''
#     for event in response.events():
#         if event.event == "add":
#             ans+=event.data
#         elif event.event == "error" or event.event == "interrupted":
#             print(event.data)
#         elif event.event == "finish":
#             pass
#         else:
#             print(event.data)
#     print(ans)