'''
pydantic 模型结构化输出，是将模型的输出转换为指定的模型实例
'''
from pydantic import BaseModel, Field

from my_llm import deepseek_llm


class Movie(BaseModel):
    title: str = Field(description="电影标题")
    director: str = Field(description="导演")
    release_date: str = Field(description="上映日期")
    rating: float = Field(description="评分")


model_with_structured_output =  deepseek_llm.with_structured_output(Movie)
resp = model_with_structured_output.invoke("推荐一部电影")
print(type(resp))
print(resp)
