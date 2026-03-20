"""
创建静态模型的agent

"""
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph.state import CompiledStateGraph

from my_llm import deepseek_llm


@tool
def get_SchoolMajor(school: str) -> str:
    """获取指定学校的专业信息"""
    return f"{school}的专业信息是：计算机科学、机械工程、电子工程等。"


agent: CompiledStateGraph = create_agent(deepseek_llm, tools=[get_SchoolMajor])

# print(type(agent))

resp : dict  = agent.invoke({"messages": [{"role":"user", "content":"请告诉我清华大学的专业信息"}]})
print(type(resp))
print(resp)
