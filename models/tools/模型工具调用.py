from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.utils import print_text

from my_llm import deepseek_llm


# LLM（大模型）使用工具返回结果的步骤
#1.定义工具，并给大模型绑定工具
#2.与LLM进行对话，LLM返回调用大模型的请求，并不会主动调用工具
#3.根据返回结果手动处理，并将结果告知LLM
#4.LLM最后生成回复

@tool
def get_weather(city: str) -> str:
    """获取天气信息"""
    # 这里可以调用第三方天气API获取天气信息
    return f"{city}的天气是晴朗，温度25度。"


# 1.绑定工具
model_bind_tool =  deepseek_llm.bind_tools([get_weather])

messages = []
human_message = HumanMessage(content="请告诉我北京的天气")
messages.append(human_message)

# 2.LLM返回调用工具的请求
resp = model_bind_tool.invoke(messages)
messages.append(resp)
for tool_call in resp.tool_calls:
    if tool_call['name'] == 'get_weather':
        # 3.根据返回结果手动处理，并将结果告知LLM
        tool_result = get_weather.invoke(tool_call)
        messages.append(tool_result)

resp = model_bind_tool.invoke(messages)
print(f"messages：{messages}")
print(resp)