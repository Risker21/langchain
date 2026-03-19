from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
# 两种方式创建大模型 对象
# 方法一：直接使用模型类
# deepseek_llm=  ChatDeepSeek(
#     api_key=DEEPSEEK_API_KEY,
#     base_url=DEEPSEEK_BASE_URL,
#     model = "deepseek-chat",
# )



# 方法二：使用模型工厂类
deepseek_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

# resp = deepseek_llm.invoke("今日璧山天气如何")
# print(type(resp))
# print(resp)
