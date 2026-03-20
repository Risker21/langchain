from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, dynamic_prompt, wrap_tool_call
from langchain_core.messages import function, ToolMessage
from langchain_core.tools import tool
from my_llm import deepseek_llm, dashscope_llm


@tool
def get_stack_price(company: str, timeframe: str = "today") -> str:
    """获取指定公司的股价信息。参数 company 是公司股票代码或名称，timeframe 是时间范围（today 或 yesterday）。"""

    # 模拟股票出错，抛出异常
    raise ValueError("股票接口不可用")


    # 模拟获取股票数据
    # mock_data = {
    #     "AAPL": {
    #         "today": "150.00 USD",
    #         "yesterday": "148.00 USD"
    #     },
    #     "GOOGL": {
    #         "today": "2800.00 USD",
    #         "yesterday": "2750.00 USD"
    #     },
    #     "HUAWEI": {
    #         "today": "200.00 USD",
    #         "yesterday": "195.00 USD"
    #     },
    #     "XIAOMI": {
    #         "today": "100.00 USD",
    #         "yesterday": "98.00 USD"
    #     }
    # }
    #
    # if company in mock_data:
    #     price = mock_data[company].get(timeframe, "未知时间范围")
    #     return f"{company}的{timeframe}股价是{price}"
    # else:
    #     return f"没有找到{company}的股价信息"


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


# 动态模型选择中间件
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler: function) -> ModelResponse:
    # 在这里可以添加任何你想要的逻辑，例如日志记录、输入输出处理等
    """根据对话次数动态选择模型"""
    # print(type(request))
    # print(request)

    message_count = len(request.state['messages'])
    if message_count >= 3:
        print("使用千问模型")
        model = dashscope_llm  # 替换为千问模型
    else:
        print("使用默认模型")
        model = deepseek_llm  # 替换为默认模型
    return handler(request.override(model=model))


# 动态提示词中间件
@dynamic_prompt
def dynamic_prompt(request: ModelRequest) -> str:
    """根据对话内容动态生成提示词"""
    print("request:", request)
    user_type = request.runtime.context.get("user_type", "normal")
    if user_type == "normal":
        prompt = "回答用户的问题之前，首先称呼：尊敬的SVIP用户，然后提供详细的股价信息和相关新闻。"
    else:
        prompt = "回答用户的问题之前，首先称呼：尊敬的普通用户，然后提供基础的股价信息和相关新闻。"
    return prompt


# 工具调用错误处理中间件
@wrap_tool_call
def handle_tool_errors(request, handler):
    """处理工具调用错误"""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            tool_call_id=request.tool_call["id"],
            content=f"工具调用出错: {str(e)}"
        )

agent = create_agent(
    model=deepseek_llm,
    tools=[get_stack_price, search_news],
    middleware=[dynamic_model_selection, dynamic_prompt, handle_tool_errors],
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "请告诉我AAPL的股价信息和新闻"}]},
    context={"user_type": "svip"},
)
print(response)
print(response["messages"][-1].content)
