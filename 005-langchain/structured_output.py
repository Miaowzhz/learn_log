from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-v4-flash",
    extra_body={"thinking": {"type": "disabled"}}
)

info = "有个同学叫张三,她是一个女生,她两年前的年龄是16岁"

message = [
    {"role": "system", "content": "你是一个学生信息提取工具,提取学生的name sex age这些信息, 请以 JSON 格式输出字符串"},
    {"role": "user", "content": info}
]

# res = llm.invoke(message)
# print(json.loads(res.text)["name"])


# class Movie(BaseModel):
#     """A movie with details."""
#     title: str = Field(description="电影标题")
#     year: int = Field(description="上映年份")
#     director: str = Field(description="导演")
#     rating: float = Field(description="电影评分")
#
# model_with_structure = llm.with_structured_output(Movie)
# response = model_with_structure.invoke("提供电影<<盗梦空间>>的详细信息")
# print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)


# from typing_extensions import TypedDict, Annotated
#
# class MovieDict(TypedDict):
#     """A movie with details."""
#     title: Annotated[str, ..., "电影标题"]
#     year: Annotated[int, ..., "上映年份"]
#     director: Annotated[str, ..., "导演"]
#     rating: Annotated[float, ..., "电影评分"]
#
# model_with_structure = llm.with_structured_output(MovieDict)
# response = model_with_structure.invoke("提供电影<<盗梦空间>>的详细信息")
# print(response)  # {'title': 'Inception', 'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.8}



json_schema = {
    "title": "Movie",
    "description": "A movie with details",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The title of the movie"
        },
        "year": {
            "type": "integer",
            "description": "The year the movie was released"
        },
        "director": {
            "type": "string",
            "description": "The director of the movie"
        },
        "rating": {
            "type": "number",
            "description": "The movie's rating out of 10"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

model_with_structure = llm.with_structured_output(
    json_schema,
    method="json_schema",
)
response = model_with_structure.invoke("提供电影<<盗梦空间>>的详细信息")
print(response)  # {'title': 'Inception', 'year': 2010, ...}


