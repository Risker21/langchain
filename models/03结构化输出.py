"""
jsonschema 结构化输出
输出json格式的字符串
"""

from my_llm import deepseek_llm


# title,description,type,properties,required五个缺一不可
json_schema = {
    "title": "Movie",
    "description": "电影的详细信息，包括标题，上映年份，导员和评分",
    "type": "object",
    "properties": {
        "title": {"type": "string","description":"电影标题"},
        "year": {"type": "string","description":"上映年份"},
        "director": {"type": "string","description":"导演"},
        "release_date": {"type": "string","description":"上映日期"},

    },
    "required": ["title", "year", "director", "release_date"],
}

model_with_structured_output = deepseek_llm.with_structured_output(json_schema)
resp = model_with_structured_output.invoke("介绍‘送你一朵小红花’这一部电影")
print(type(resp))
print(resp)

