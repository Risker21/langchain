"""
pydantic 模型结构化输出
输出dict字典类型
"""
from typing import TypedDict, Annotated

from my_llm import deepseek_llm


class Movie(TypedDict):
    title: Annotated[str, "电影标题"]
    director: Annotated[str, "导演"]
    release_date: Annotated[str, "上映日期"]
    rating: Annotated[float, "电影评分"]


model_with_structured_output = deepseek_llm.with_structured_output(Movie)
resp = model_with_structured_output.invoke("送你一朵小红花是一部什么样的电影")
print(type(resp))
print(resp)
