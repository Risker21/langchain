from langchain_core.tools import tool

from my_llm import deepseek_llm


@tool
def get_weather(city: str) -> str:
    """获取天气信息"""
    # 这里可以调用第三方天气API获取天气信息
    return f"{city}的天气是晴朗，温度25度。"


model_bind_tool =  deepseek_llm.bind(get_weather)
resp = model_bind_tool.invoke("请告诉我北京的天气")
print(type(resp))
print(resp)