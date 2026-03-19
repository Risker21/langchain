from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from my_llm import deepseek_llm


# LLM（大模型）使用工具返回结果的步骤
# 1.定义工具，并给大模型绑定工具
# 2.与LLM进行对话，LLM返回调用大模型的请求，并不会主动调用工具
# 3.根据返回结果手动处理，并将结果告知LLM
# 4.LLM最后生成回复

@tool
#
def get_stack_price(company: str, timeframe: str = "today") -> str:
    """获取指定公司的股价信息。参数 company 是公司股票代码或名称，timeframe 是时间范围（today 或 yesterday）。"""
    mock_data = {
        "AAPL": {
            "today": "150.00 USD",
            "yesterday": "148.00 USD"
        },
        "GOOGL": {
            "today": "2800.00 USD",
            "yesterday": "2750.00 USD"
        },
        "HUAWEI": {
            "today": "200.00 USD",
            "yesterday": "195.00 USD"
        },
        "XIAOMI": {
            "today": "100.00 USD",
            "yesterday": "98.00 USD"
        }
    }

    if company in mock_data:
        price = mock_data[company].get(timeframe, "未知时间范围")
        return f"{company}的{timeframe}股价是{price}"
    else:
        return f"没有找到{company}的股价信息"


@tool
def search_news(company: str) -> str:
    """搜索关于特定公司的最新新闻。参数 company 是公司名称。"""
    mock_news = {
        "AAPL": ["苹果公司发布了新的iPhone型号，预计将引起市场热潮。",
                 "苹果公司宣布了一项新的环保计划，致力于减少碳足迹。",
                 "苹果公司在全球范围内扩展了其服务业务，预计将带来更多收入。"],
        "GOOGL": ["谷歌宣布了一项新的人工智能计划，旨在推动AI技术的发展。",
                  "谷歌发布了新的搜索算法更新，预计将改善用户体验。",
                  "谷歌在云计算领域取得了重大突破，预计将提升市场竞争力。"],
        "HUAWEI": ["华为推出了最新的5G手机，受到了消费者的广泛关注。",
                   "华为宣布了一项新的全球合作计划，旨在推动技术创新。"
                   "华为在智能家居领域取得了重大进展，预计将提升市场份额。"],
        "XIAOMI": ["小米公司发布了新的智能家居产品线，预计将提升市场份额。",
                   "小米公司宣布了一项新的全球扩展计划，旨在进入更多国际市场。"
                   "小米在智能手机领域取得了重大突破，预计将提升市场竞争力。"]

    }
    new_list = mock_news.get(company, [f"没有找到{company}的相关新闻"])
    return "\n".join(new_list)


# 1.绑定工具
model_bind_tool = deepseek_llm.bind_tools([get_stack_price, search_news])

messages = []
human_message = HumanMessage(content="HUAWEI今天的股价是多少？")
messages.append(human_message)

# 2.LLM返回调用工具的请求
while True:
    response = model_bind_tool.invoke(messages)
    messages.append(response)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call['name'] == 'get_stack_price':
                # 3.根据返回结果手动处理，并将结果告知LLM
                tool_result = get_stack_price.invoke(tool_call)
                messages.append(tool_result)
            elif tool_call['name'] == 'search_news':
                tool_result = search_news.invoke(tool_call)
                messages.append(tool_result)

    else:
        print("无工具调用")
        break # 如果没有工具调用，说明LLM已经生成了最终回复，可以退出循环

print(f"messages：{messages}")
print(response.tool_calls)
