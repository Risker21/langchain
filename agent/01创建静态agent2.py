from langchain.agents import create_agent
from langchain_core.tools import tool
from my_llm import deepseek_llm
@tool
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
    """搜索关于特定公司的最新新闻。参数 company 是公司名称。mock_news是一个模拟的新闻数据字典，包含了每个公司的最新新闻列表。函数根据输入的公司名称返回对应的新闻，如果没有找到相关信息，则返回一个提示消息。"""
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
        "XIAOMI": ["小米公司发布了新的智能家居产品线，预计将提升市场份。",
                   "小米公司宣布了一项新的全球扩展计划，旨在进入更多国际市场。"
                   "小米在智能手机领域取得了重大突破，预计将提升市场竞争力。"]

    }
    new_list = mock_news.get(company, [f"没有找到{company}的相关新闻"])
    return "\n".join(new_list)

agent = create_agent(
    model=deepseek_llm,
    tools=[get_stack_price, search_news]
)

resp : dict  = agent.invoke({"messages": [{"role":"user", "content":"请告诉我AAPL的股价信息和新闻"}]})
print(type(resp))
print(resp)