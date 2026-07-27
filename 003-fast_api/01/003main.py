"""

响应格式
HTML格式
File格式
自定义响应

异常响应处理

"""


from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/get_html", response_class=HTMLResponse)
async def get_html():
    return HTMLResponse("<h1>这是HTML格式</h1>")

@app.get("/get_file")
async def get_file():
    return FileResponse("003main.py")

class News(BaseModel):
    id: int
    title: str
    content: str

# 自定义响应
@app.get("/get_news")
async def get_news(id: int):
    return {
        "id": id,
        "title": "这是新闻标题",
        "content":"这是新闻内容"
    }

# 异常响应处理
@app.get("/get_username")
async def get_username(username: str):
    username_list = ["admin", "user"]
    if username == "":
        raise HTTPException(status_code=400, detail="用户名不能为空")
    if username not in username_list:
        raise HTTPException(status_code=404, detail="用户名不存在")
    return {"username": username}