from fastapi import FastAPI, Path

# 创建 FastAPI 实例
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World666"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/user/hello")
async def say_hello():
    return {"message": "我正在学习 FastAPI"}

# @app.get("/book/{book_id}")
# async def get_book(book_id: int):
#     return {"book_id": book_id, "title": f"这是第{book_id}本书"}

@app.get("/book/{book_id}")
async def get_book(book_id: int = Path(..., ge=1, le=100, description="书籍编号,1-100")):
    return {"book_id": book_id, "title": f"这是第{book_id}本书"}


@app.get("/news/{n_id}")
async def get_news(n_id: int = Path(..., ge=1, le=100, description="新闻编号,1-100")):
    return {"news_id": n_id, "title": f"这是第{n_id}条新闻"}

@app.get("/news/get/{n_name}")
async def get_news_name(n_name: str = Path(..., min_length=2, max_length=10)):
    return {"news_name": f"新闻的名字是{n_name}"}